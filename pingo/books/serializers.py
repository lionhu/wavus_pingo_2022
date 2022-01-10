from rest_flex_fields import FlexFieldsModelSerializer
from .models import Publisher, Author, Tag, Book


class PublisherSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id", "name", "city", "state_province", "country",
                  "website", "latitude", "longitude",)


class AuthorSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "salutation", "name", "email", "headshot",)


class TagSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title",)


class BookSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "summary", "authors",
                  "publisher", "publication_date", "state",
                  "isbn", "price", "pages", "stock_count", "tags",)
        expandable_fields = {  # expandable_fieldsでネスト
            "publisher": PublisherSerializer,
            "authors": (AuthorSerializer, {"many": True}),  # 多対多
            "tags": (TagSerializer, {"many": True})  # 多対多
        }
