from templated_mail.mail import BaseEmailMessage
from core.functions import PrintExceptionError
__all__ = [
    "Supplier_NewOrderItemEmail",
    "Superadmin_NewOrderEmail",
    "Member_NewOrderEmail",
]


class Supplier_NewOrderItemEmail(BaseEmailMessage):
    template_name = "email/supplier/orders/new_notification.html"

    def get_context_data(self):
        print("Supplier_NewOrderItemEmail get_context_data")
        context = super().get_context_data()
        context["subject"] = context.get("subject")
        context["type"] = context.get("type")
        context["content"] = context.get("content")

        context["orderitem_id"] = context.get("orderitem_id")
        context["item_name"] = context.get("item_name")
        context["username"] = context.get("username")
        context["variation_name"] = context.get("variation_name")
        context["quantity"] = context.get("quantity")

        context["button_blue_text"] = context.get("button_blue_text")
        context["button_blue_url"] = context.get("button_blue_url")
        context["button_grey_text"] = context.get("button_grey_text")
        context["button_grey_url"] = context.get("button_grey_url")
        return context


class Superadmin_NewOrderEmail(BaseEmailMessage):
    template_name = "email/superadmin/orders/new_notification.html"

    def get_context_data(self):
        print("Superadmin_NewOrderItemEmail get_context_data")
        context = super().get_context_data()
        context["subject"] = context.get("subject")
        context["type"] = context.get("type")
        context["content"] = context.get("content")

        context["order_id"] = context.get("order_id")
        context["username"] = context.get("username")
        context["quantity"] = context.get("quantity")
        context["total"] = context.get("total")

        context["button_blue_text"] = context.get("button_blue_text")
        context["button_blue_url"] = context.get("button_blue_url")
        context["button_grey_text"] = context.get("button_grey_text")
        context["button_grey_url"] = context.get("button_grey_url")
        return context


class Member_NewOrderEmail(BaseEmailMessage):
    template_name = "email/member/orders/new_notification.html"

    def get_context_data(self):
        print("Member_NewOrderEmail get_context_data")
        context = super().get_context_data()
        context["subject"] = context.get("subject")
        context["type"] = context.get("type")
        context["content"] = context.get("content")

        context["order"] = context.get("order")
        context["orderitems"] = context.get("orderitems")

        context["button_blue_text"] = context.get("button_blue_text")
        context["button_blue_url"] = context.get("button_blue_url")
        context["button_grey_text"] = context.get("button_grey_text")
        context["button_grey_url"] = context.get("button_grey_url")
        return context

    # def send(self, to, *args, **kwargs):
    #     try:
    #         super().send(to, *args, **kwargs)
    #     except Exception as err:
    #          print("Member_NewOrderEmail error:")
    #          print(PrintExceptionError(err))
