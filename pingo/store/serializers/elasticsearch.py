from rest_framework.serializers import ModelSerializer
from store.models import Item, Variation, PointBank, Favorite, ViewProductHistory, Comment, Category
import logging
from django.contrib.auth import get_user_model

logger = logging.getLogger("error_logger")
User = get_user_model()

__all__ = [
    "DynamicSearchSerializer",
    "UserElasticSearchSerializer",
    "CategoryElasticSearchSerializer",
    "ItemElasticSearchSerializer",
    "VariationElasticSearchSerializer",
    "ItemSimpleElasticSearchSerializer",
    "PointBankElasticSearchSerializer",
    "FavoriteElasticSearchSerializer",
    "ViewProductHistoryElasticSearchSerializer",
    "CommentElasticSearchSerializer",
]


class DynamicSearchSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        omit_fields = self.context.get('omit_fields', None)
        print("__init__ FavoriteElasticSearchSerializer")
        print(omit_fields)
        if omit_fields:
            for field_name in omit_fields:
                self.fields.pop(field_name)


class UserElasticSearchSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'avatar_thumb_url',
            'email'
        )


class CategoryElasticSearchSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
        )


class ItemElasticSearchSerializer(ModelSerializer):
    category = CategoryElasticSearchSerializer(many=False)

    class Meta:
        model = Item
        fields = (
            'id',
            'item_name',
            'description',
            'package',
            'is_valid',
            "thumbimage_url",
            "category",
            "labels",
            "variation_min_price",
            "variation_stock_total",
            "supplier_indexing",
            "sort_by",
        )


# class VariationElasticSearchSerializer(ModelSerializer):
#     category = CategoryElasticSearchSerializer(many=False)

#     class Meta:
#         model = Item
#         fields = (
#             'id',
#             'item_name',
#             'description',
#             'package',
#             'is_valid',
#             "thumbimage_url",
#             "category",
#             "labels",
#             "variation_min_price",
#             "variation_stock_total",
#             "supplier_indexing",
#             "sort_by",
#         )


class ItemSimpleElasticSearchSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'item_name',
            'description',
            'package',
            'is_valid',
            "thumbimage_url",
            "category_indexing",
            "labels",
            "variation_min_price",
            "variation_stock_total",
            "supplier_indexing",
            "sort_by",
        )


class PointBankElasticSearchSerializer(ModelSerializer):
    class Meta:
        model = PointBank
        fields = (
            'id',
            'point',
            'until_at',
            'created_at'
        )


class FavoriteElasticSearchSerializer(DynamicSearchSerializer):
    item = ItemSimpleElasticSearchSerializer(many=False)
    user = UserElasticSearchSerializer(many=False)

    class Meta:
        model = Favorite
        fields = (
            'id',
            'item',
            "user",
            'created_at'
        )

    def to_representation(self, instance):
        result = super(FavoriteElasticSearchSerializer,
                       self).to_representation(instance)
        if "item" in result:
            result["item"].pop("labels")
            result["item"].pop("description")
            result["item"].pop("package")
        return result


class ViewProductHistoryElasticSearchSerializer(DynamicSearchSerializer):
    item = ItemSimpleElasticSearchSerializer(many=False)
    user = UserElasticSearchSerializer(many=False)

    class Meta:
        model = ViewProductHistory
        fields = (
            'id',
            'item',
            "user",
            'type',
            'created_at'
        )


class CommentElasticSearchSerializer(DynamicSearchSerializer):
    item = ItemSimpleElasticSearchSerializer(many=False)
    user = UserElasticSearchSerializer(many=False)

    class Meta:
        model = Comment
        fields = (
            'id',
            'item',
            "user",
            'item_type',
            'content',
            'rate',
            'thumbs_down',
            'thumbs_up',
            'approved',
            'checked',
            'created_at',
        )


class VariationElasticSearchSerializer(DynamicSearchSerializer):
    item = ItemSimpleElasticSearchSerializer(many=False)

    class Meta:
        model = Variation
        fields = (
            'id',
            'item',
            'name',
            'description',
            'thumbimage_url',
            'purchase_price',
            'extra_cost',
            'price',
            'is_valid',
            'sort_by',
            'inventory',
            'sku',
            'point_rule',
        )
