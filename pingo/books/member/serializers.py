from rest_flex_fields import FlexFieldsModelSerializer
from books.models import Publisher, Author, Tag, Book

import logging

logger = logging.getLogger("error_logger")


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

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(BookSerializer, self).__init__(*args, **kwargs)

        omit_fields = self.context.get('omit_fields', None)

        if omit_fields:
            omitted = set(omit_fields)
            for field_name in omitted:
                self.fields.pop(field_name)

        # fields = self.context['request'].query_params.get('fields')
        # if fields:
        #     fields = fields.split(',')
        #     allowed = set(fields)
        #     existing = set(self.fields.keys())
        #     for field_name in existing - allowed:
        #         self.fields.pop(field_name)

    def to_representation(self, *args, **kwargs):
        # logger.error("to_representation")
        # logger.error(self.context.get("exclude_email_list",{}))
        # logger.error(self.context)
        result = super().to_representation(*args, **kwargs)

        return result
