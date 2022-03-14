from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from store.models import Category, Faq, Section, Logistic, Supplier, AddressBook
from rolepermissions.checkers import has_role
from djoser.serializers import UserSerializer

__all__ = [
    "ContextFlexFieldsModelSerialier",

    "CategorySerializer",
    "FaqSerializer",
    "SectionSerializer",
    "LogisticSerializer",
    "SupplierSerializer",
    "AddressBookSerializer"
]


class ContextFlexFieldsModelSerialier(FlexFieldsModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context:
            self._context = getattr(self.Meta, 'context', {})

        try:
            self.user = self.context["request"].user
        except KeyError:
            self.user = None

    def get_fields(self):
        fields = super().get_fields()

        if self.user is not None and has_role(self.user, ["superadmin"]):
            return fields

        if hasattr(self.Meta, "private_fields") and len(self.Meta.private_fields) > 0:
            for field_name in self.Meta.private_fields:
                fields.pop(field_name)

        return fields


class CategorySerializer(serializers.ModelSerializer):
    # full_name = SerializerMethodField("get_full_name")
    access = serializers.JSONField(required=False)
    badge = serializers.JSONField(required=False)

    class Meta:
        model = Category
        fields = ('id', 'title', "is_valid", "sort_by", 'children', 'parent', 'isTitle', "isMenuCollapsed",
                  "access", "sort_by", "icon", "badge", "link", "regular_product_count", "pingo_product_count",)

    def to_representation(self, instance):
        result = super(CategorySerializer, self).to_representation(instance)

        if "children" in result and len(result["children"]) == 0:
            result.pop("children")

        return result


CategorySerializer._declared_fields['children'] = CategorySerializer(
    many=True, source='get_children', read_only=True)


class FaqSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Faq
        fields = ("id", "question", "answer", "is_valid", "index", "section",)


class SectionSerializer(FlexFieldsModelSerializer):
    faqs = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ('id', 'title', "index", 'is_valid', "faqs",)
        read_only_fields = ("faqs",)

    def get_faqs(self, instance):
        logger.error("get_faqs")
        user = self.context["request"].user
        if has_role(user, "staff") or has_role(user, "superadmin"):
            _faqs = Faq.objects.filter(section=instance)
        else:
            _faqs = Faq.objects.filter(section=instance, is_valid=True)
        serializer = FaqSerializer(_faqs, many=True)
        return serializer.data


class LogisticSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Logistic
        fields = ('id', 'company', "short_name", 'is_valid', "track_link",)


class SupplierSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', 'name', "email", 'website', 'phone', "postcode", "state",
                  "town", "city", "address_1", "address_2", "user", 'is_valid',)
        expandable_fields = {  # expandable_fieldsでネスト
            "user": (UserSerializer, {"many": False}),  # 多対多
        }


class AddressBookSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = AddressBook
        fields = ('id', 'user', 'name', "email", 'phone', "postcode", "state",
                  "town", "city", "address_1", "address_2",)
        expandable_fields = {  # expandable_fieldsでネスト
            "user": (UserSerializer, {"many": False}),  # 多対多
        }
