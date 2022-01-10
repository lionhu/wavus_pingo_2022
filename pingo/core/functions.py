from pingo.conf import settings as pingo_settings
import shutil
import os
import re
from PIL import Image
import qrcode
from io import BytesIO
import traceback
from django.core.files.uploadedfile import InMemoryUploadedFile
import logging

logger = logging.getLogger("error_logger")


def PrintExceptionError(error):
    trace_back = traceback.format_exc()
    logger.error(str(trace_back))
    message = str(error)
    if pingo_settings.SYSTEM["PrintExceptionTrace"]:
        message = str(error) + " " + str(trace_back)

    return message


def suqre_crop_image(imagefield, temp_imagefile):
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


def remove_image_file(file_image, is_include_folder=False):
    try:
        path = file_image.path
        if os.path.exists(path):
            if is_include_folder:
                folder = os.path.dirname(path)
                shutil.rmtree(folder)
                logger.error(f"delete images folder: {folder}")

            else:
                storage = file_image.storage
                storage.delete(path)
                logger.error(f"delete image filename {path}.")
    except Exception as err:
        logger.error("something wrong when deleting files or folder")


def full_path_redis_key(request, prefix, pk):
    full_path = request.get_full_path()
    logger.error(full_path)
    full_path.replace("{", "1")
    full_path.replace("}", "2")
    full_path.replace("[]", "3")
    full_path.replace("&", "4")
    full_path.replace("=", "5")
    logger.error(full_path)
    if full_path.find("?"):
        redis_list_keys = "{}_{}".format(prefix, full_path.split("?")[1])
    else:
        redis_list_keys = "{}".format(prefix)
    if pk:
        redis_list_keys = "{}_{}".format(pk, redis_list_keys)

    return redis_list_keys


def generate_user_product_qr(user, product, service_type):
    slug = user.introcode
    filename = os.path.join("mediafiles/introcode_qrs/users/user_{}_intro_qr.png".format(str(slug)))
    url = "{}/account/register?introcode={}&p_type={}&pid={}".format(pingo_settings.NICHIEI_INFO["WEBSITE"],
                                                                     slug, service_type, product.id)
    merge_filename = "mediafiles/introcode_qrs/merges/{}_{}_product_{}.jpg".format(user.id, service_type,product.id)

    productImage = Image.open(product.image)
    product_width, product_height = productImage.size
    logger.error("product.thumbimage_large: {},{}".format(product_width, product_height))

    if not os.path.exists(merge_filename):
        if not os.path.exists(filename):
            qr = qrcode.QRCode(box_size=2)
            qr.add_data(url)
            qr.make()
            img_qr = qr.make_image()
            big_qr = img_qr.resize((240, 240))
            big_qr.save(filename)

        qr_image = Image.open(filename)
        qr_image_width, qr_image_height = qr_image.size
        logger.error("qr_image_width > product_width: {},{}".format(qr_image_width, product_width))
        if qr_image_width > product_width:
            wpercent = qr_image_width / qr_image_height
            new_qr_height = int(qr_image_height * float(wpercent))
            qr_image = qr_image.resize((product_width, new_qr_height), Image.ANTIALIAS)

        introcode_bg_image = Image.open("mediafiles/introcode_bg.jpg")
        new_image = Image.new("RGB", (productImage.size[0], productImage.size[1] + 255), (250, 250, 250))
        new_image.paste(productImage, (0, 255))
        new_image.paste(introcode_bg_image, (0, 0))
        new_image.paste(qr_image, (5, 5))
        new_image.save(merge_filename, "JPEG")

    return {
        "merge_pic": "{}/{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], merge_filename),
        "share_link": url
    }


def extract_query_param_filter(param_string):
    low_param = param_string.lower()
    logger.error(low_param)
    if "filter" in low_param:
        result = re.search(r"\{([A-Za-z0-9_]+)\}", param_string)
        logger.error(result)
        logger.error(result.group(1))
        return result.group(1)
    return None
