from pingo.conf import settings as pingo_settings
import shutil
import os
from PIL import Image
from io import BytesIO
from rolepermissions.checkers import has_role
from django.core.cache import cache
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile
import logging

logger = logging.getLogger("error_logger")


class PingoImageMixin:
    def replace_instance_old_images(self, instance, imagefile):
        self.remove_instance_old_images(instance)

        tempfile = "{}.jpg".format(uuid.uuid4())
        user_avatar = self.suqre_crop_image(imagefile, tempfile)
        instance.image = user_avatar
        instance.save()

    def suqre_crop_image(self, imagefield, temp_imagefile):
        img = Image.open(imagefield)
        DEFAULT_IMAGE_SIZE = pingo_settings.DEFAULT_IMAGE_SIZE

        crop_box = ()
        if img._size[0] > img._size[1]:
            inset = (img._size[0] - img._size[1]) // 2
            crop_box = (inset, 0, inset + img._size[1], img._size[1])
        elif img._size[1] > img._size[0]:
            inset = (img._size[1] - img._size[0]) // 2
            crop_box = (0, inset, img._size[0], inset + img._size[0])

        if crop_box:
            img = img.crop(box=crop_box)
            logger.error("crop image")

        if img.height > DEFAULT_IMAGE_SIZE or img.width > DEFAULT_IMAGE_SIZE:
            output_size = (DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_SIZE)
            logger.error("limit image size ")
            img.thumbnail(output_size)

        logger.error(f"crop square image:{img.height}")
        buffer = BytesIO()
        img.save(fp=buffer, format='JPEG')
        buffer.seek(0)

        output_imagefield = InMemoryUploadedFile(buffer, None, temp_imagefile, 'image/jpeg', buffer.tell, None)
        return output_imagefield

    def remove_image_file(self, file_image, is_include_folder=False):

        try:
            path = file_image.path
            if os.path.exists(path):
                if is_include_folder:
                    logger.error(f"delete folder: {path}")
                    folder = os.path.dirname(path)
                    shutil.rmtree(folder)
                    logger.error(f"delete images folder: {folder}")

                else:
                    storage = file_image.storage
                    storage.delete(path)
                    logger.error(f"delete image filename {path}.")
        except Exception as err:
            logger.error("something wrong when deleting files or folder")

    def remove_instance_old_images(self, instance):
        try:
            if str(instance.image) != pingo_settings.DEFAULT_IMAGE:
                if os.path.exists(instance.image.path):
                    self.remove_image_file(instance.image)
                    logger.error("remove old user avatar")
                if os.path.exists(instance.thumbimage.path):
                    self.remove_image_file(instance.thumbimage, True)
                    logger.error("remove old user avatar thumbimage")
        except Exception as err:
            logger.error("something wrong when deleting files or folder")


class RedisMixin:
    # example
    # prefix_redis = pingo_settings.REDIS_KEYS["VIEW_HISTORIES"].format(request.user.id)
    # cached_data = self.get_redis_data(prefix_redis, request)
    #
    # if pingo_settings.USE_REDIS_CACHE:
    #     if cached_data is None:
    #         self.filters = {
    #             "user": request.user.id
    #         }
    #         response = super(self.__class__, self).list(request, *args, **kwargs)
    #         cached_data = response.data
    #         self.set_redis_data(prefix_redis, request, cached_data, 300)
    # else:
    #     response = super(self.__class__, self).list(request, *args, **kwargs)
    #     cached_data = response.data
    #
    # return Response(cached_data, status=status.HTTP_200_OK)

    @staticmethod
    def get_redis_key(prefix, request):
        logger.error(request.query_params)
        redis_key = prefix
        if has_role(request.user, ["superadmin", "staff", "supplier"]):
            redis_key = "management_" + redis_key
        else:
            redis_key = "public_" + redis_key

        for param in request.query_params:
            query_value = request.query_params.get(param, None)
            redis_key = redis_key + "_" + str(param) + "_" + str(query_value)

        return redis_key

    def get_redis_data(self, prefix, request):
        redis_key = self.get_redis_key(prefix, request)
        if redis_key != "":
            return cache.get(redis_key, None)
        return None

    def set_redis_data(self, prefix, request, data, timeout):
        redis_key = self.get_redis_key(prefix, request)
        if redis_key != "":
            cache.set(redis_key, data, timeout)
            return self.get_redis_data(prefix, request)
        return None

    def remove_pattern_redis_cache(self, pattern):
        logger.error(f"remove_pattern_redis_cache: *{pattern}*")
        cache.delete_pattern(f"*{pattern}*")


class DynamicQuerySetMixin:
    omit_fields = None

    def get_expand_fields(self):
        if len(self.request.query_params) > 0:
            if "omit" in self.request.query_params:
                query_value = self.request.query_params.get("expand", None)
                self.omit_fields = query_value.split(",")

    def get_omit_fields(self):
        if len(self.request.query_params) > 0:
            if "omit" in self.request.query_params:
                query_value = self.request.query_params.get("omit", None)
                self.omit_fields = query_value.split(",")
                print("get omit fields")
                print(self.omit_fields )
