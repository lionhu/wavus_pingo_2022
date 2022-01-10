# from django.contrib import admin
# import logging
# from .models import *
#
# logger = logging.getLogger("error_logger")
#
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#
#     list_display = ('title', 'isbn', 'price', 'publication_date')
#     search_fields = ('title',)
#     filter_horizontal = ('authors', 'tags',)
#     actions = ["test_pingo"]
#
#     def test_pingo(self,request, queryset):
#         logger.error(request.user)
#         logger.error(queryset)
#
#
# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#
#     list_display = ('name', 'email',)
#     search_fields = ('name',)
#
#
# @admin.register(Publisher)
# class PublisherAdmin(admin.ModelAdmin):
#
#     list_display = ('name',)
#     search_fields = ('name',)
#
#
# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#
#     list_display = ('title',)
#     search_fields = ('title',)
