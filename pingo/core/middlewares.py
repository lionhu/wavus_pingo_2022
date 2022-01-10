from PIL import Image
from io import BytesIO
from pingo.conf import settings as pingo_settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import logging

logger = logging.getLogger("error_logger")


def expand_square(self, pil_img, background_color):
    print("expand_square")
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def resize_square(imagefile):
    logger.error("resize_square")
    try:
        im = Image.open(imagefile)
        width, height = im.size
        target_temp_size = max(width, height)
        target_size = min(pingo_settings.SYSTEM.DEFAULT_IMAGE_SIZE, target_temp_size)

        im_thumb = expand_square(im, (255, 255, 255)).resize((target_size, target_size), Image.LANCZOS)
        buffer = BytesIO()
        im_thumb.save(fp=buffer, format='JPEG')
        buff_val = buffer.getvalue()
        return ContentFile(buff_val)
    except Exception as err:
        logger.error("resize square image failed")


class SquareSizeImageMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)

        return response

    def process_request(self, request):
        logger.error("リクエストの処理")
        logger.error(request)
        logger.error(request.FILES)
        if request.FILES is not None:
            try:
                square_image = resize_square(request.FILES["image"])
                image_file = InMemoryUploadedFile(square_image, None, 'foo.jpg', 'image/jpeg', square_image.tell, None)
                request.FILES["image"] = square_image
            except Exception as err:
                pass


    def process_response(self, request, response):
        logger.error("レスポンスの処理")
