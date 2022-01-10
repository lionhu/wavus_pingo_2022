from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from authentication.models import LoggedInUser, Profile, Client

User = get_user_model()

__all__ = [
    "UserDocument",
    "LoggedInUserDocument",
    "ProfileDocument",
]


@registry.register_document
class UserDocument(Document):
    avatar_thumb_url = fields.TextField(attr="avatar_thumb_url")
    last_location_indexing = fields.TextField(attr="last_location_indexing")
    roles_indexing = fields.TextField(attr="roles_indexing")

    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'introcode',
            'parent_introcode',
            'last_login',
            'login_count',
            'is_active',
        ]


@registry.register_document
class LoggedInUserDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'email': fields.TextField(),
        'avatar_thumb_url': fields.TextField(attr="avatar_thumb_url")
    })

    class Index:
        name = 'active_users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = LoggedInUser
        related_models = [User]
        fields = [
            'id',
            'web',
            'ws_channel',
            'created_at',
        ]

    def get_queryset(self):
        return super(LoggedInUserDocument, self).get_queryset().select_related(
            'user'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.logged_in_user


@registry.register_document
class ProfileDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'email': fields.TextField(),
        'introcode': fields.TextField(),
        'parent_introcode': fields.TextField(),
        'avatar_thumb_url': fields.TextField(attr="avatar_thumb_url"),
        'last_login': fields.DateField(),
        'login_count': fields.IntegerField(),
        'is_active': fields.BooleanField(),
    })

    client = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    parent_indexing = fields.IntegerField(attr="parent_indexing")
    get_descendants_count = fields.IntegerField(attr="get_descendants_count")

    class Index:
        name = 'profiles'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Profile
        related_models = [User,Client]
        fields = [
            'id',
            'can_transfer_point',
        ]

    def get_queryset(self):
        return super(ProfileDocument, self).get_queryset().select_related(
            'user'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.profile
        elif isinstance(related_instance, Client):
            return related_instance.profile_set.all()
