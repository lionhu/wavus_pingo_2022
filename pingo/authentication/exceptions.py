from rest_framework.exceptions import APIException
from rest_framework import status
from django.contrib.auth import get_user_model
from pingo.conf import settings as pingo_settings
import logging

logger = logging.getLogger("error_logger")

User = get_user_model()


class OneClientExecption(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Only one client is allowed to one user"
    default_code = "one_client_permission"


class SystemAssetExecption(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "System asset can not be touched"
    default_code = "system_asset_permission"


class NoAccessExecption(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "NoAccess right to excute"
    default_code = "no_access_right"

