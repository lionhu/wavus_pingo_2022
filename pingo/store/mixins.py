from rolepermissions.checkers import has_role
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .exceptions import GenerateOrderError_InsufficientPoint, GenerateOrderError_CreditCardFailed, \
    Cancel_CreditCard_Payment_Failed
from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from pingo.conf import settings as pingo_settings
from django.contrib.auth import get_user_model
from core.functions import extract_query_param_filter, PrintExceptionError
from store.models import Variation, OrderItem, Margin, PointBank
from django.db.models import F, Sum, Count
from django.db.models.functions import TruncDay, TruncMonth
from square.client import Client
import uuid
import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


class OrderPointDistribution:
    def __init__(self, order):
        self.order = order
        self.WAVUSADMIN = User.objects.get(username=pingo_settings.SUPERUSER)
        self.WAVUSMASTER = User.objects.get(username=pingo_settings.WAVUS_CLIENT_NAME)
        self.user = order.user
        self.client = self.user.profile.client
        self.parent = None
        self.grandparent = None
        self.ClientAdmin = None
        self.SuperClientAdmin = None

        self.find_margin_chain_user()

    def check_SYSTEM_ADMIN(self, user):
        if user.username == pingo_settings.SUPERUSER:
            return True
        elif user.username == pingo_settings.WAVUS_CLIENT_NAME:
            return True

        return False

    def find_margin_chain_user(self):
        if self.user is not None:
            if not self.check_SYSTEM_ADMIN(self.user.profile.parent.user):
                self.parent = self.user.profile.parent.user

            if self.parent and not self.check_SYSTEM_ADMIN(self.parent.profile.parent.user):
                self.grandparent = self.parent.profile.parent.user

            if self.user.profile.client and not self.check_SYSTEM_ADMIN(self.user.profile.client.admin):
                self.ClientAdmin = self.user.profile.client.admin

            if self.user.profile.client and self.client.client_superadmin:
                self.SuperClientAdmin = self.client.client_superadmin

        chain_users = {}
        if self.user:
            chain_users.update({"user": self.user})
        if self.parent:
            chain_users.update({"parent": self.parent})
        if self.grandparent:
            chain_users.update({"grandparent": self.grandparent})
        if self.ClientAdmin:
            chain_users.update({"ClientAdmin": self.ClientAdmin})
        if self.SuperClientAdmin:
            chain_users.update({"SuperClientAdmin": self.SuperClientAdmin})

        logger.error("distribute points, chain_users")
        logger.error(chain_users)
        return chain_users

    def distribute_order_points(self):
        orderitems = OrderItem.objects.filter(order=self.order)

        if orderitems.exists():
            for orderitem in orderitems:
                variation, quantity = orderitem.variation, orderitem.quantity

                if variation.point_rule["is_valid"]:
                    self.distribute_amount_point(variation, quantity, orderitem)

    def distribute_amount_point(self, variation, quantity, orderitem):
        try:
            margin_policy = self.client.margin_policy
            if pingo_settings.SHOP_SETTINGS["FORCE_USE_SYSTEM_MARGIN_POLICY"]:
                margin_policy = pingo_settings.SHOP_SETTINGS["DEFAULT_MARGIN_POLICY"]

            logger.error("finally applied margin_policy")
            logger.error(margin_policy)

            user_self_point = int(variation.point_rule["policies"]["user_self"])
            parent_point = int(variation.point_rule["policies"]["level_1"])
            grantparent_point = int(variation.point_rule["policies"]["level_2"])
            clientadmin_point = int(variation.point_rule["policies"]["client_admin"])
            superclientadmin_point = int(variation.point_rule["policies"]["client_superadmin"])

            if self.user and margin_policy["USER_SELF"] and user_self_point:
                self.distribute_point(self.user, user_self_point * quantity, orderitem, "USER_SELF")

            if self.parent and margin_policy["LEVEL_1"] and parent_point:
                self.distribute_point(self.parent, parent_point * quantity, orderitem, "LEVEL_1")

            if self.grandparent and margin_policy["LEVEL_2"] and grantparent_point:
                self.distribute_point(self.grandparent, grantparent_point * quantity, orderitem, "LEVEL_2")

            if self.ClientAdmin and margin_policy["CLIENTADMIN"] and clientadmin_point:
                self.distribute_point(self.ClientAdmin, clientadmin_point * quantity, orderitem, "CLIENTADMIN")

            if self.SuperClientAdmin and margin_policy["SUPERADMIN"] and superclientadmin_point:
                self.distribute_point(self.SuperClientAdmin, superclientadmin_point * quantity, orderitem, "SUPERADMIN")

        except KeyError:
            pass

    def distribute_point(self, user, amount, orderitem, level_type):

        # logger.error("self.bought_policy({}, {})".format(user.id, orderitem.item_id))
        # if user and self.bought_policy(user.id, orderitem.item_id):
        logger.error("distribute_point to: {} with point: {},level_type:{}".format(user, amount, level_type))
        Margin.objects.create(
            user=user,
            amount=amount,
            type="OrderBonus" if level_type == "USER_SELF" else "DesendentOrderPoint",
            is_refound=1,
            is_valid=False,
            from_orderID=self.order.id,
            fromuser=self.order.user,
            info={
                "username": self.order.user.username,
                "order_id": self.order.id,
                "orderitem_id": orderitem.id,
                "variation_id": orderitem.variation.id,
                "level": level_type
            }
        )

    def distribute_pingoOrder_point(self):
        margin_policy = self.client.margin_policy
        if pingo_settings.SHOP_SETTINGS["FORCE_USE_SYSTEM_MARGIN_POLICY"]:
            margin_policy = pingo_settings.SHOP_SETTINGS["DEFAULT_MARGIN_POLICY"]

        logger.error("finally applied margin_policy")
        logger.error(margin_policy)

        user_self_point = int(self.order.product.point_rule["policies"]["user_self"])
        if self.user and margin_policy["USER_SELF"] and self.order.product.point_rule["is_valid"] and user_self_point:
            Margin.objects.create(
                user=self.user,
                amount=user_self_point * self.order.quantity,
                type="OrderBonus",
                order_type="PINGO",
                is_refound=1,
                is_valid=False,
                from_orderID=self.order.id,
                fromuser=self.user,
                info={
                    "username": self.user.username,
                    "order_id": self.order.id,
                    "level": "USER_SELF"
                }
            )


class DynamicQuerySetMixin:
    dynamic_queryset = True
    model_class = None
    sorted_by = ()

    def get_redis_key_by_role(self, redis_key):
        if self.request.user == AnonymousUser():
            return f"PUBLIC_{redis_key}"

        user = self.request.user
        if has_role(user, "client") or has_role(user, "member") or has_role(user, "client_superadmin"):
            return f"MEMBER_{redis_key}"
        elif has_role(user, "superadmin") or has_role(user, "staff"):
            return f"PRIVATE_{redis_key}"
        elif has_role(user, "supplier"):
            return f"SUPPLIER_{redis_key}"

    def set_query_filters(self):
        print("set_query_filters")
        print(self.request.query_params)
        if len(self.request.query_params) > 0:
            print(self.request.query_params)
            for param in self.request.query_params:
                _filter = extract_query_param_filter(param)
                if _filter:
                    query_value = self.request.query_params.get(param, None)
                    if "_id" not in _filter:
                        self.filters.update({_filter: query_value})
                    else:
                        if int(query_value) > 0:
                            self.filters.update({_filter: int(query_value)})

    def set_query_sorted_by(self):
        if "sorted_by" in self.request.query_params and len(self.request.query_params["sorted_by"]) > 0:
            self.sorted_by = tuple(self.request.query_params["sorted_by"].split(","))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        self.set_query_filters()

        if hasattr(self, "filters") and len(self.filters) > 0:
            print("setting .filters")
            queryset = self.model_class.objects.filter(**self.filters)
        else:
            print("remove .filters")
            queryset = self.model_class.objects.all()

        print("filters")
        print(self.filters)
        print(queryset)

        self.set_query_sorted_by()
        if hasattr(self, "sorted_by") and len(self.sorted_by):
            print(f"*self.sorted_by:{self.sorted_by}")
            print(f"len(self.sorted_by):{len(self.sorted_by)}")
            queryset = queryset.order_by(*self.sorted_by)

        return queryset


# class RedisMixin:
# example
# prefix_redis = pingo_settings.REDIS_KEYS["VIEW_HISTORIES"].format(request.user.id)
# cached_data = self.get_redis_data(prefix_redis, request)
#
# if pingo_settings.USE_REDIS_CACHE:
#     if cached_data is None:
#         self.filters = {
#             "user": request.user.id
#         }
#         response = super(self.__class__, self).list(request, *args, **kwargs)
#         cached_data = response.data
#         self.set_redis_data(prefix_redis, request, cached_data, 300)
# else:
#     response = super(self.__class__, self).list(request, *args, **kwargs)
#     cached_data = response.data
#
# return Response(cached_data, status=status.HTTP_200_OK)

# @staticmethod
# def get_redis_key(prefix, request):
#     logger.error(request.query_params)
#     redis_key = prefix
#     if has_role(request.user, ["superadmin", "staff", "supplier"]):
#         redis_key = "management_" + redis_key
#     else:
#         redis_key = "public_" + redis_key
#
#     for param in request.query_params:
#         query_value = request.query_params.get(param, None)
#         redis_key = redis_key + "_" + str(param) + "_" + str(query_value)
#
#     return redis_key
#
# def get_redis_data(self, prefix, request):
#     redis_key = self.get_redis_key(prefix, request)
#     if redis_key != "":
#         return cache.get(redis_key, None)
#     return None
#
# def set_redis_data(self, prefix, request, data, timeout):
#     redis_key = self.get_redis_key(prefix, request)
#     if redis_key != "":
#         cache.set(redis_key, data,timeout)
#         return self.get_redis_data(prefix, request)
#     return None
#
# def remove_pattern_redis_cache(self, pattern):
#     logger.error(f"remove_pattern_redis_cache: *{pattern}*")
#     cache.delete_pattern(f"*{pattern}*")


class SquarePaymentMixin:

    def pay_order_byCreditCard(self, order_type, order, nonce):
        logger.error("SquarePaymentMixin order id: {}, with nonce: {}".format(order.id, nonce))
        try:
            client = Client(access_token=pingo_settings.SQUARE_PAYMENT["ACCESSTOKEN"],
                            environment=pingo_settings.SQUARE_PAYMENT["ENV"])

            locations_api = client.locations
            result = locations_api.list_locations()
            if result.is_success():
                idempotency_key = str(uuid.uuid1())
                amount = {'amount': order.chargeAmount, 'currency': 'JPY'}
                body = {'idempotency_key': idempotency_key,
                        'source_id': nonce,
                        'amount_money': amount,
                        "autocomplete": False,
                        "note": f"{order_type}_order_#{order.id}"
                        }

                logging.info("credit card charge, order:{}".format(order.id))
                logging.info("amount:{}".format(amount))

                api_response = client.payments.create_payment(body)
                if api_response.is_success():
                    res = api_response.body['payment']
                    logger.error("payment_info id: {}".format(res["id"]))

                    return {"result": True,
                            "order": order,
                            "payment_status": res["status"],
                            "payment_id": res["id"],
                            "payment_details": res,
                            "message": "Square Payment Successfully placed."}

                elif api_response.is_error():
                    res = "Exception when calling PaymentsApi->create_payment: {}".format(api_response.errors)
                    raise GenerateOrderError_CreditCardFailed
                    # return {"result": False, "order": None, "payment_info": {}, "message": res}
        except Exception as err:
            raise GenerateOrderError_CreditCardFailed
            # return {"result": False, "order": None, "payment_info": {}, "message": PrintExceptionError(err)}

    def order_cancel_payment(self, payment_id):
        logger.error("SquarePaymentMixin cancel payment_id: {}".format(payment_id))
        try:
            client = Client(access_token=pingo_settings.SQUARE_PAYMENT["ACCESSTOKEN"],
                            environment=pingo_settings.SQUARE_PAYMENT["ENV"])

            locations_api = client.locations
            result = locations_api.list_locations()
            if result.is_success():
                api_response = client.payments.cancel_payment(payment_id)
                if api_response.is_success():
                    res = api_response.body['payment']
                    logger.error("successfully canceled payment_info id: {}".format(res["id"]))

                    return {"result": True,
                            "payment_status": res["status"],
                            "payment_id": res["id"],
                            "payment_details": res,
                            "message": "Square Payment Successfully canceled."}

                elif api_response.is_error():
                    res = "Exception when calling PaymentsApi->create_payment: {}".format(api_response.errors)
                    logger.error("failed to cancel creditcard payment")
                    logger.error(res)
                    raise Cancel_CreditCard_Payment_Failed
        except Exception as err:
            logger.error("failed to cancel creditcard payment")
            logger.error(PrintExceptionError(err))
            raise Cancel_CreditCard_Payment_Failed

    def order_complete_payment(self, payment_id):
        logger.error("SquarePaymentMixin complete payment_id: {}".format(payment_id))
        try:
            client = Client(access_token=pingo_settings.SQUARE_PAYMENT["ACCESSTOKEN"],
                            environment=pingo_settings.SQUARE_PAYMENT["ENV"])

            locations_api = client.locations
            result = locations_api.list_locations()
            if result.is_success():
                api_response = client.payments.complete_payment(payment_id)
                if api_response.is_success():
                    res = api_response.body['payment']
                    logger.error("successfully completed payment_info id: {}".format(res["id"]))

                    return {"result": True,
                            "payment_status": res["status"],
                            "payment_id": res["id"],
                            "payment_details": res,
                            "message": "Square Payment Successfully canceled."}

                elif api_response.is_error():
                    res = "Exception when calling PaymentsApi->create_payment: {}".format(api_response.errors)
                    logger.error(res)
                    raise GenerateOrderError_CreditCardFailed
        except Exception as err:
            logger.error(PrintExceptionError(err))
            raise GenerateOrderError_CreditCardFailed


class OrderMixin:
    @staticmethod
    def check_variation_stock(variation_id, quantity):
        variation = Variation.objects.get(pk=variation_id)
        if variation.inventory >= quantity:
            logger.error("variation.inventory >= quantity")
            return True
        return False

    def check_order_inventory(self, cart_items):
        order_validate = True
        if cart_items:
            for cart_item in cart_items:
                variation = cart_item["variant"]
                quantity = cart_item["quantity"]
                variation_check = self.check_variation_stock(variation["id"], quantity)
                if not variation_check:
                    order_validate = False
                cart_item["validate"] = variation_check

        return {
            "cart_items": cart_items,
            "order_validate": order_validate
        }

    def check_order_data(self, order_data):
        point_usage = order_data.get("point_usage", None)
        chargeAmount = order_data.get("chargeAmount", 0)
        Total = order_data.get("Total", 0)
        nonce = order_data.get("nonce", None)

        pay_by_point = bool(point_usage["apply_point"])
        cart_use_point = int(point_usage["use_point"]) if pay_by_point else 0

        stock_check_validation = self.check_order_inventory(order_data["cart_items"])
        if not stock_check_validation["order_validate"]:
            raise ValidationError("insufficient stock")

        if chargeAmount == 0:
            if not pay_by_point:
                raise ValidationError("pay_by_point is false?")
            elif cart_use_point < Total:
                raise ValidationError("not enough point to pay order")
        elif 0 < chargeAmount < Total:
            if chargeAmount + cart_use_point != Total:
                raise ValidationError("credit cart and  point does not equal total")

            if not nonce:
                raise ValidationError("nonce is required")

        if chargeAmount == Total and not nonce:
            raise ValidationError("nonce is required")


class PointBankMixin:

    def check_SYSTEM_ADMIN(self, user):
        if user.username == pingo_settings.SUPERUSER:
            return True
        elif user.username == pingo_settings.WAVUS_CLIENT_NAME:
            return True

        return False

    def distribute_introduction_point(self, user, order):
        introduct_point = pingo_settings.SHOP_SETTINGS["INTRODUCE_POINT_POLICY"]

        if introduct_point == 0:
            # if not introduction_point availalbe, quit
            return False

        parent = user.profile.parent.user if user.profile.parent else None
        if self.check_SYSTEM_ADMIN(user.profile.parent.user) or parent is None:
            # there is no introduction bonus for admin users
            return False

        if "introduction_point_paid" not in parent.profile.extra_info:
            parent.profile.extra_info["introduction_point_paid"] = []

        paid_list = parent.profile.extra_info["introduction_point_paid"]

        if paid_list.count(user.id):
            logger.error("parent {} has already get introduce point from".format(parent.username, user.username))
        else:
            margin = Margin.objects.create(
                user=parent,
                type="INTRODUCE_POINT",
                is_valid=False,
                is_refound=True,
                amount=introduct_point,
                from_orderID=order.id,
                fromuser=user,
                info={"user_id": user.id,
                      "username": user.username,
                      "order_id": order.id,
                      "order_type": order.type}
            )
            parent.profile.extra_info["introduction_point_paid"].append(user.id)
            parent.profile.save()

    def distribute_self_join_point(self, user, order):
        join_bonus_point = pingo_settings.SHOP_SETTINGS["JOIN_BONUS_POLICY"]

        if join_bonus_point == 0:
            return False

        extra_info = user.profile.extra_info
        logger.error("init extra_info")
        logger.error(extra_info)

        if "join_bonus" not in extra_info or not extra_info["join_bonus"]:
            logger.error("extra_info not in extra_info or not extra_info[join_bonus]")
            margin = Margin.objects.create(
                user=user,
                type="JOINBONUS_POINT",
                is_valid=False,
                is_refound=True,
                amount=pingo_settings.SHOP_SETTINGS["JOIN_BONUS_POLICY"],
                from_orderID=order.id,
                fromuser=user,
                info={"user_id": user.id,
                      "username": user.username,
                      "order_id": order.id,
                      "order_type": order.type}
            )
            user.profile.extra_info["join_bonus"] = True
            user.profile.save()

    def batch_withdraw_introduction_point(self, order_ids):
        for order_id in order_ids:
            logger.error("withdraw_introduction_point:{}".format(order_id))
            self.withdraw_introduction_point(order_id)

    def batch_withdraw_self_join_point(self, order_ids):
        for order_id in order_ids:
            logger.error("batch_withdraw_self_join_point:{}".format(order_id))
            self.withdraw_self_join_point(order_id)

    def withdraw_introduction_point(self, order_id):
        try:

            margin = Margin.objects.filter(from_orderID=order_id, type="INTRODUCE_POINT").first()

            logger.error("try to remove {} introduction from order_id:{}".format(margin.fromuser_id, order_id))
            if margin:
                parent_profile = margin.user.profile
                if parent_profile.extra_info and parent_profile.extra_info["introduction_point_paid"]:
                    extra_info = parent_profile.extra_info["introduction_point_paid"]
                    new_introduction_list = extra_info.remove(margin.fromuser_id)
                    parent_profile.extra_info[
                        "introduction_point_paid"] = new_introduction_list if new_introduction_list else []
                    parent_profile.save()
                    logger.error(" to remove {} introduction from order_id:{}".format(margin.fromuser_id, order_id))
        except Exception as err:
            logger.error("failed to remove introduction from order_id:{}".format(order_id))

    def withdraw_self_join_point(self, order_id):
        try:
            margin = Margin.objects.filter(from_orderID=order_id, type="JOINBONUS_POINT").first()

            if margin:
                user_profile = margin.user.profile
                if user_profile.extra_info and user_profile.extra_info["join_bonus"]:
                    user_profile.extra_info["join_bonus"] = False
                    user_profile.save()
                    logger.error(" to remove {} join_bonus from order_id:{}".format(margin.user_id, order_id))
        except Exception as err:
            logger.error(" failed to  remove {} join_bonus from order_id:{}".format(margin.user_id, order_id))

    def create_pointbank_from_margin(self, margin):
        try:
            if margin and margin.is_valid and margin.is_refound == 1 and margin.pointbank_saved is False:
                pointbank = PointBank.objects.filter(margin=margin)
                if not pointbank.exists():
                    PointBank.objects.create(
                        user=margin.user,
                        point=margin.amount,
                        info={
                            "margin_id": margin.id,
                            # "order_type": margin.order_type
                        },
                        margin=margin
                    )
                    margin.pointbank_saved = True
                    margin.save()
                    logger.error("create pointbank with valid params")
        except Exception as error:
            logger.error("Failed to create pointbank")
            logger.error(PrintExceptionError(error))

    def create_pointbank_from_margins(self, margins):
        try:
            for margin in margins:
                self.create_pointbank_from_margin(margin)
        except Exception as error:
            logger.error("Failed to batch create pointbank")
            return Response({
                "message": PrintExceptionError(error)
            }, status=status.HTTP_400_BAD_REQUEST)

    def pointbank_use_point(self, user_id, point):

        try:
            logger.error("pointbank_use_point:user_id {}, point:{}".format(user_id, point))

            pointbanks = PointBank.objects.filter(user_id=user_id).order_by("until_at")
            if not pointbanks.exists():
                return False

            temp_point = point
            for pointbank in pointbanks:
                if pointbank.point == temp_point:
                    pointbank.delete()
                    logger.error("remove == pointbank_{}, point:{}".format(pointbank.id, temp_point))
                    break
                if pointbank.point > temp_point:
                    pointbank.point = pointbank.point - temp_point
                    pointbank.save()
                    logger.error("remove > pointbank_{}, point:{}".format(pointbank.id, temp_point))
                    break
                else:
                    temp_point = temp_point - pointbank.point
                    pointbank.delete()
                    logger.error("remove < pointbank_{}, point:{}".format(pointbank.id, temp_point))
        except Exception as error:
            logger.error("Failed to batch create pointbank")
            logger.error(PrintExceptionError(error))

    def pointbank_user_totalpoint(self, user_id):
        try:
            logger.error("pointbank_user_totalpoint user_id:{}".format(user_id))
            mp = PointBank.objects.filter(user_id=user_id).aggregate(total=Sum("point"))
            logger.error(mp)
            return mp["total"] if mp["total"] else 0
        except Exception as error:
            logger.error(PrintExceptionError(error))
            return 0

    def has_enough_points(self, user_id, points):
        logger.error("pointbank_user_totalpoint user_id:{}".format(user_id))
        mp = PointBank.objects.filter(user_id=user_id).aggregate(total=Sum("point"))
        userpoints = int(mp["total"]) if int(mp["total"]) else 0
        return userpoints >= points

    def pointbank_user_pointsummary(self, user_id):
        try:
            summary = PointBank.objects.filter(user_id=user_id).annotate(due_date=TruncMonth("until_at")).values(
                "due_date").annotate(
                count=Count("id"), sum=Sum("point")).order_by("due_date")
            json_summary = []
            if summary.exists():
                for each_line in summary:
                    json_summary.append({
                        "due_date": each_line["due_date"],
                        "count": each_line["count"],
                        "sum": each_line["sum"]})
            return json_summary
        except Exception as error:
            logger.error(PrintExceptionError(error))
            return ""

    def refound_canceled_pingoOrder(self, order):
        refound_margin = Margin.objects.create(
            type="ORDER_CANCELED",
            order_type="PINGO",
            user=order.user,
            fromuser=order.user,
            amount=order.total,
            is_valid=True,
            is_refound=1,
            from_orderID=order.id,
            pointbank_saved=False,
            info={"order_id": order.id}
        )
        self.create_pointbank_from_margin(refound_margin)


class RemoveProductRedisKeyMixin:
    def remove_redis_product(self, request):
        item_id = request.data.get("item", None)
        logger.error(f"{self.model_class} create")
        if item_id:
            product_key = pingo_settings.REDIS_KEYS["PRODUCT"].format(item_id)
            cache.delete(product_key)
            logger.error(f"remove:{product_key}")

    def create(self, request, *args, **kwargs):
        self.remove_redis_product(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.remove_redis_product(request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.remove_redis_product(request)
        return super().destroy(request, *args, **kwargs)
