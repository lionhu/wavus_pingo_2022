from django.utils.functional import LazyObject
from django.test.signals import setting_changed
from django.conf import settings as django_settings
from django.utils.module_loading import import_string


class ObjDict(dict):
    def __getattribute__(self, item):
        try:
            val = self[item]
            if isinstance(val, str):
                val = import_string(val)
            elif isinstance(val, (list, tuple)):
                val = [import_string(v) if isinstance(v, str) else v for v in val]
            self[item] = val
        except KeyError:
            val = super(ObjDict, self).__getattribute__(item)

        return val


PINGO_SETTINGS_NAMESPACE = "PINGO"
SETTINGS_TO_IMPORT = []

GROUPS_SUPERADMIN = ["pingo.roles.Superadmin"]
GROUPS_STAFF = ["pingo.roles.Superadmin", "pingo.roles.Staff"]
GROUPS_PRIVATE = ["pingo.roles.Superadmin", "pingo.roles.Staff", "pingo.roles.Supplier"]
GROUPS_PUBLIC = ["pingo.roles.Superadmin", "pingo.roles.Staff", "pingo.roles.Member"]
MARGIN_POLICY = {
    # "POLICIES": {
    "SUPERADMIN": False,
    "CLIENTADMIN": True,
    "LEVEL_1": True,
    "LEVEL_2": True,
    "USER_SELF": True,
    "SELF_BOUGHT": {
        "APPLY": False,
        "LIMIT": 3
    }
    # }
}

default_settings = {
    "WEBSITE": "https://www.pingo.jp",
    "ADMIN_ID": 1,
    "ADMIN_CLIENT_ID": 1,
    "ADMIN_EMAIL": "huhaiguang@me.com",
    "SUPERUSER": "SUPERADMIN",
    "WAVUS_GROUP_NAME": "WAVUS_GROUP",
    "SUPPLIER_GROUP_NAME": "SUPPLIER_GROUP",
    "WAVUS_CLIENT_NAME": "WAVUS_CLIENT",
    "SYSTEM_USER_NAMES": ["SUPERADMIN", "WAVUS_GROUP", "SUPPLIER_GROUP", "WAVUS_CLIENT", ],
    "SYSTEM_CLIENT_NAMES": ["WAVUS_CLIENT", ],

    "LAST_ACTIVITY_INTERVAL_SECS": 600,
    "USER_LAST_LOGIN": "USER_{}_LAST_LOGIN",

    "DEFAULT_IMAGE": "default.jpg",
    "DEFAULT_IMAGE_SIZE": 800,

    "SEND_ACTIVATION_EMAIL": False,
    "SEND_CONFIRMATION_EMAIL": True,
    "SITE_NAME": "lionhu master",
    "BOOK_MODEL": "books.models.book",
    "SERIALIZERS": ObjDict(
        {
            "activation": "djoser.serializers.ActivationSerializer",
        }
    ),
    "VALID_PRODUCT_LOOKUP": {
        'is_valid': True,
    },
    "NICHIEI_INFO": {
        "WEBSITE": "https://www.pingo.jp",
        "SALES_EMAIL": "crs@wavus.jp",
        "SALES_PHONE": "+81 50-3697-9239 ",
        "SALES_MAN_PHONE": "+81 50-3697-9239 ",
        "SALES_POSTCODE": "〒104-0061 東京都中央区",
        "SALES_ADD": "銀座1-12-4N&E BLD.7階",
        "CONTACT_INFO_EMAIL": "huhaiguang@me.com"
    },
    "SYSTEM": ObjDict({
        "PrintExceptionTrace": True,
        "DEFAULT_IMAGE_SIZE": 800,
        "ROOT_MENU": "ROOT_MENU",
    }),
    "SHOP_SETTINGS": ObjDict({
        "FORCE_USE_SYSTEM_MARGIN_POLICY": False,
        "ROOT_SHOP_MENU": "ROOT_SHOP_MENU",
        "DEFAULT_MARGIN_POLICY": MARGIN_POLICY,
        "INTRODUCE_POINT_POLICY": 1000,
        "JOIN_BONUS_POLICY": 1000,
        "POINT_EXPIRE_DAYS": 365,
    }),
    "SQUARE_PAYMENT": ObjDict({
        "ACCESSTOKEN": "EAAAEKn7YWyd9RxfRvOlkCUNexEIREbG-7f-bLQyJ4oY4b0QlKrU8FsFJjIeUYDr",
        "ENV": "sandbox",
        "APPID": "sandbox-sq0idb-W7v96oQuEI-T1jDlEXuNWA",

        # "ACCESSTOKEN":"EAAAEO9vaObx-tl4ftlGLxGTv6RvNEGiivGfIAg7lgk6uQCsB_r1cmmvkrSjObtq",
        # "ENV":"production",
        # "APPID":"sq0idp-tpOzmEV17j6Ond43x0vdUg",
    }),
    "USE_REDIS_CACHE": True,
    "REDIS_KEYS": {
        "CATEGORIES": "shop_categories",
        "PRODUCT": "product_{}",
        "PUBLIC_PRODUCT": "public_product_{}",
        "ADMIN_PRODUCT": "admin_product_{}",

        "PUBLIC_CATEGORY_PRODUCT": "public_category_{}_products",
        "ADMIN_CATEGORY_PRODUCT": "admin_category_{}_products",

        "STORE_NEW_PRODUCTLIST": "store_new_products",
        "STORE_BESTSELLER_PRODUCTLIST": "store_bs_products",
        "CATEGORY_PRODUCTS": "category_{}_products",
        "USER_PRODUCT_SHARE_QRCODE": "sharecode_user_{}_product_{}",
        "PRODUCT_COMMENTS": "product_{}_comments",
        "COMMENT": "comment_{}",
        "MY_FAVORITES": "user_{}_favorites",
        "VIEW_HISTORIES": "user_{}_view_products",

        "PUBLIC_PINGO_PRODUCT": "public_pingo_product_{}",
        "ADMIN_PINGO_PRODUCT": "admin_pingo_product_{}",
        "USER_PINGO_PRODUCT_SHARE_QRCODE": "sharecode_user_{}_pingo_product_{}",
    },
    "ELASTICSEARCH_INDEX_NAMES": {
        'store.documents': 'item',
        'authentication.documents': 'user',
    },

    "SEND_SUPERADMIN_COMMENT_CREATED_EMAIL": True,
    "SEND_SUPERADMIN_NEW_ORDER_EMAIL": True,
    "SEND_MEMBER_NEW_ORDER_EMAIL": True,
    "SUPPLIER_AUTO_SEND_NEW_ORDERITEM_EMAIL": True,
    "EMAIL": ObjDict(
        {
            "common_notification": "store.emails.CommonNotificationEmail",

            "new_comment_notification": "store.emails.NewCommentEmail",

            "supplier_new_orderitem_notification": "store.emails.Supplier_NewOrderItemEmail",

            "superadmin_new_order_notification": "store.emails.Superadmin_NewOrderEmail",

            "member_new_order_notification": "store.emails.Member_NewOrderEmail",
        }
    ),
    "TASKS": ObjDict(
        {

            "common_notification": "store.tasks.common_notification",


            "notify_supplier_orderitem": "store.tasks.notify_supplier_orderitem",
            "notify_supplier_orderitem_batch": "store.tasks.notify_supplier_orderitem_batch",

            "notify_superadmin_new_order": "store.tasks.notify_superadmin_new_order",
            "notify_superadmin_new_order_batch": "store.tasks.notify_superadmin_new_order_batch",

            "notify_member_new_order": "store.tasks.notify_member_new_order",
        }
    ),
}


class Settings:
    def __init__(self, default_settings, explicit_overriden_settings: dict = None):
        if explicit_overriden_settings is None:
            explicit_overriden_settings = {}

        overriden_settings = (
                getattr(django_settings, PINGO_SETTINGS_NAMESPACE, {})
                or explicit_overriden_settings
        )

        self._load_default_settings()
        self._override_settings(overriden_settings)
        self._init_settings_to_import()

    def _load_default_settings(self):
        for setting_name, setting_value in default_settings.items():
            if setting_name.isupper():
                setattr(self, setting_name, setting_value)

    def _override_settings(self, overriden_settings: dict):
        for setting_name, setting_value in overriden_settings.items():
            value = setting_value
            if isinstance(setting_value, dict):
                value = getattr(self, setting_name, {})
                value.update(ObjDict(setting_value))
            setattr(self, setting_name, value)

    def _init_settings_to_import(self):
        for setting_name in SETTINGS_TO_IMPORT:
            value = getattr(self, setting_name)
            if isinstance(value, str):
                setattr(self, setting_name, import_string(value))


class LazySettings(LazyObject):
    def _setup(self, explicit_overriden_settings=None):
        self._wrapped = Settings(default_settings, explicit_overriden_settings)


settings = LazySettings()


def reload_pingo_settings(*args, **kwargs):
    global settings
    setting, value = kwargs["setting"], kwargs["value"]
    print("reload_pingo_settings")
    print(setting)
    print(value)
    if setting == PINGO_SETTINGS_NAMESPACE:
        settings._setup(explicit_overriden_settings=value)


setting_changed.connect(reload_pingo_settings)
