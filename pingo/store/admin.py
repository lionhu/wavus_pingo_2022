from django.contrib import admin
from store.models import Category, Item, ItemSliderImage, Variation, \
    Supplier, Faq, Section, Logistic, Comment, Favorite, PingoItem, PingoItemSliderImage, \
    Order, OrderItem, PointBank, Margin
from mptt.admin import MPTTModelAdmin
from django.utils.html import format_html
import os


class CategoryMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


class ItemPingoSliderImageInline(admin.StackedInline):
    model = PingoItemSliderImage
    fields = ("title", "http_referer", "type", "image", "thumbimage",)
    readonly_fields = ('thumbimage',)
    extra = 1

    def thumbimage(self, instance):
        if instance.image:
            tmpl = '<img style="max-width:60px;" src="{}" onClick="window.open(\'{}\', \'{}\');" />'
            basename = os.path.basename(instance.image.url)
            return format_html(
                tmpl, instance.thumbimage.url, instance.image.url, basename)


class PingoItemAdmin(admin.ModelAdmin):
    inlines = [ItemPingoSliderImageInline]
    list_display = ("item_name", "category", "is_valid", "targetNum", "currentNum", "until_at", "thumbimage")
    list_filter = ('status', 'category')
    list_editable = ("is_valid",)
    # thumbnail = AdminThumbnail(image_field='thumbimage')
    fieldsets = [
        ("製品", {'fields': [('item_name', "is_valid", "rate"), ]}),
        ("基本情報", {'fields': [("category", "labels"), ]}),
        ("イベント情報", {'fields': [("targetNum", "currentNum", "until_at"), ]}),
        ('写真', {'fields': [('image', "thumbimage",)]}),
        ("メーカー", {'fields': [('supplier'), ("brand", "series", "model"), ], 'classes': ['collapse']}),
        ('製品紹介', {'fields': [('description'), ], 'classes': ['collapse']}),
        ('パッケージ', {'fields': [('package'), ], 'classes': ['collapse']}),
        ('ポイント', {'fields': [('point_rule'), ]}),
    ]
    readonly_fields = ('thumbimage',)

    def thumbimage(self, instance):
        if instance.image:
            tmpl = '<img style="max-width:60px;" src="{}" onClick="window.open(\'{}\', \'{}\');" />'
            basename = os.path.basename(instance.image.url)
            return format_html(
                tmpl, instance.thumbimage.url, instance.image.url, basename)


class ItemSliderImageInline(admin.StackedInline):
    model = ItemSliderImage
    fields = ("title", "http_referer", "type", "image", "thumbimage",)
    readonly_fields = ('thumbimage',)
    extra = 1

    def thumbimage(self, instance):
        if instance.image:
            tmpl = '<img style="max-width:60px;" src="{}" onClick="window.open(\'{}\', \'{}\');" />'
            basename = os.path.basename(instance.image.url)
            return format_html(
                tmpl, instance.thumbimage.url, instance.image.url, basename)


class VariationInline(admin.StackedInline):
    model = Variation
    fields = (
        "name", "description", "price", "purchase_price", "inventory", "point_rule", "image", "thumbimage", "type",)
    readonly_fields = ('thumbimage',)
    extra = 1

    def thumbimage(self, instance):
        if instance.image:
            tmpl = '<img style="max-width:60px;" src="{}" onClick="window.open(\'{}\', \'{}\');" />'
            basename = os.path.basename(instance.image.url)
            return format_html(
                tmpl, instance.thumbimage.url, instance.image.url, basename)


class ItemAdmin(admin.ModelAdmin):
    inlines = [VariationInline, ItemSliderImageInline]
    list_display = ("item_name", "is_valid", "brand", "series", "category", "thumbimage")
    list_filter = ('type', 'category')
    list_editable = ("is_valid",)
    # thumbnail = AdminThumbnail(image_field='thumbimage')
    fieldsets = [
        ("製品", {'fields': [('item_name', "is_valid", "rate"), ]}),
        ("基本情報", {'fields': [("category", "labels"), ]}),
        ('写真', {'fields': [('image', "thumbimage",)]}),
        ("メーカー", {'fields': [('supplier'), ("brand", "series", "model"), ], 'classes': ['collapse']}),
        ('製品紹介', {'fields': [('description')], 'classes': ['collapse']}),
        ('パッケージ', {'fields': [('package')], 'classes': ['collapse']}),
    ]
    readonly_fields = ('thumbimage',)

    def thumbimage(self, instance):
        if instance.image:
            tmpl = '<img style="max-width:60px;" src="{}" onClick="window.open(\'{}\', \'{}\');" />'
            basename = os.path.basename(instance.image.url)
            return format_html(
                tmpl, instance.thumbimage.url, instance.image.url, basename)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "user",)


class FaqInline(admin.StackedInline):
    model = Faq
    fields = ("index", "is_valid", "question", "answer",)
    readonly_fields = ("section",)


class SectionAdmin(admin.ModelAdmin):
    inlines = [FaqInline]
    list_display = ("index", "is_valid", "title",)
    fields = ("index", "is_valid", "title",)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    fields = ("variation", "quantity", "final_price", "status", "delivered",
              "delivered_at", "delivery_info", "logistic", "paid", "paid_at", "paid_info",)


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("user", "status", "ordered_at", "Qty", "Total", "chargeAmount",)
    fields = ("user", "status", "ordered_at", "Qty", "Total", "chargeAmount",)
    readonly_fields = ("ordered_at",)


class LogisticAdmin(admin.ModelAdmin):
    list_display = ("is_valid", "company", "short_name",)
    fields = ("is_valid", "company", "short_name", "track_link",)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "created_at",)
    fields = ("user", "item", "metadata", "created_at",)


class PointBankAdmin(admin.ModelAdmin):
    list_display = ("user", "point", "until_at",)
    fields = ("user", "margin", "point", "info", "until_at",)
    readonly_fields = ("created_at",)


class MarginAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "order_type", "amount", "is_valid","pointbank_saved", "fromuser", "created_at",)
    fields = ("user", "type", "order_type", "amount", "is_valid", "fromuser",
              "is_refound", "paid_at", "info", "from_orderID",)
    readonly_fields = ("created_at",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "rate", "thumbs_up", "thumbs_down", "approved", "created_at",)
    fields = ("user", "item", "content", "rate", "thumbs_up", "thumbs_down", "approved", "created_at",)
    readonly_fields = ("created_at",)

admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(PingoItem, PingoItemAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Logistic, LogisticAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PointBank, PointBankAdmin)
admin.site.register(Margin, MarginAdmin)
