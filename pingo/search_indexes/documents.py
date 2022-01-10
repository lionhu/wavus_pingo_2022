from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from books.models import Book

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="kuromoji_tokenizer",
    filter=["lowercase", "stop", "snowball", "kuromoji_part_of_speech",
            "kuromoji_stemmer", "kuromoji_baseform", "kuromoji_readingform"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class BookDocument(Document):
    id = fields.IntegerField(attr='id')

    title = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
        },
        fielddata="true"
    )

    description = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
        },
        fielddata="true"
    )

    summary = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
        },
        fielddata="true"
    )

    publisher = fields.TextField(
        attr='publisher_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
        },
        fielddata="true"
    )

    publication_date = fields.DateField()

    state = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
        },
        fielddata="true"
    )

    isbn = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
        },
        fielddata="true"
    )

    price = fields.FloatField(
        fields={
            'raw': fields.IntegerField(),
        }
    )

    pages = fields.IntegerField()

    stock_count = fields.IntegerField()

    tags = fields.TextField(
        attr='tags_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(multi=True),
            'suggest': fields.CompletionField(multi=True),
        },
        fielddata="true",
        multi=True
    )

    class Django(object):
        model = Book
