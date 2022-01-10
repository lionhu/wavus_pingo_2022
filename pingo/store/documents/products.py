from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django.contrib.auth import get_user_model
from store.models import Item, PointBank, Favorite, ViewProductHistory, Comment, Category, Variation

User = get_user_model()

__all__ = [
    "ProductDocument",
    "PointBankDocument",
    "FavoriteDocument",
    "ProductCommentDocument",
    "ViewProductHistoryDocument",
    "VariationDocument",
]


class UserInnerDoc(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'email': fields.TextField(),
        'avatar_thumb_url': fields.TextField(attr="avatar_thumb_url")
    })


class ItemInnerDoc(Document):
    item = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'item_name': fields.TextField(),
        'description': fields.TextField(),
        'package': fields.TextField(),
        'is_valid': fields.BooleanField(),
        'thumbimage_url': fields.TextField(attr="thumbimage_url"),
        'category_indexing': fields.TextField(),
        "labels": fields.TextField(),
        "variation_min_price": fields.IntegerField(attr="variation_min_price"),
        'variation_stock_total': fields.IntegerField(attr="variation_stock_total"),
        "supplier_indexing": fields.TextField(),
        "sort_by": fields.IntegerField(),
    })


@registry.register_document
class VariationDocument(ItemInnerDoc):
    thumbimage_url = fields.TextField(attr='thumbimage_url')
    point_rule_indexing = fields.TextField(attr="point_rule_indexing")

    class Index:
        name = 'variations'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Variation
        related_models = [Item]
        fields = [
            'id',
            'is_valid',
            'name',
            'description',
            'price',
            'purchase_price',
            'extra_cost',
            'inventory',
            'sku',
            'sort_by',
            'updated_at',
        ]

    def get_queryset(self):
        return super(VariationDocument, self).get_queryset().select_related(
            'item'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Item):
            return related_instance.item_variations.all()


@registry.register_document
class ProductDocument(Document):
    thumbimage_url = fields.TextField(attr='thumbimage_url')
    supplier_indexing = fields.TextField(attr='supplier_indexing')
    # category_to_string = fields.TextField(attr='category_to_string')
    category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'title': fields.TextField(),
    })
    labels = fields.TextField()
    variation_min_price = fields.IntegerField(attr="variation_min_price")
    variation_stock_total = fields.IntegerField(attr="variation_stock_total")

    class Index:
        name = 'items'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Item
        related_models = [Category]
        fields = [
            'id',
            'item_name',
            'description',
            'package',
            'is_valid',
            'sort_by',
        ]

    def get_queryset(self):
        return super(ProductDocument, self).get_queryset().select_related(
            'category'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.category_items.all()


@registry.register_document
class PointBankDocument(UserInnerDoc):
    class Index:
        name = 'pointbanks'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = PointBank
        related_models = [User]
        fields = [
            'id',
            'point',
            'until_at',
            'created_at',
        ]

    def get_queryset(self):
        return super(PointBankDocument, self).get_queryset().select_related(
            'user'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.validpointbank.all()


@registry.register_document
class FavoriteDocument(UserInnerDoc, ItemInnerDoc):
    class Index:
        name = 'favorites'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Favorite
        related_models = [User, Item]
        fields = [
            'id',
            'created_at',
        ]

    def get_queryset(self):
        return super(FavoriteDocument, self).get_queryset().select_related(
            'user',
            'item',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.user_favorites.all()
        elif isinstance(related_instance, Item):
            return related_instance.item_favorites.all()


@registry.register_document
class ProductCommentDocument(UserInnerDoc, ItemInnerDoc):
    class Index:
        name = 'product_comments'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Comment
        related_models = [User, Item]
        fields = [
            'id',
            'item_type',
            'content',
            'rate',
            'thumbs_down',
            'thumbs_up',
            'approved',
            'checked',
            'created_at',
        ]

    def get_queryset(self):
        return super(ProductCommentDocument, self).get_queryset().select_related(
            'user',
            'item',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.user_comments.all()
        elif isinstance(related_instance, Item):
            return related_instance.item_comments.all()


@registry.register_document
class ViewProductHistoryDocument(UserInnerDoc, ItemInnerDoc):
    class Index:
        name = 'viewproducts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = ViewProductHistory
        related_models = [User, Item]
        fields = [
            'id',
            'created_at',
            'type'
        ]

    def get_queryset(self):
        return super(ViewProductHistoryDocument, self).get_queryset().select_related(
            'user',
            'item',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.viewproducts.all()
        elif isinstance(related_instance, Item):
            return related_instance.viewproducthistory_set.all()
