from rest_framework.exceptions import APIException
from rest_framework import status
import logging

logger = logging.getLogger("error_logger")


class NoAdminAccessPermission(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "No permission to execute operation."
    default_code = "no_access_permission"


class GenerateOrderError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "ERROR occurred while creating order "
    default_code = "generate_order_error"


class GenerateOrderError_InsufficientPoint(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Insufficient available points"
    default_code = "insufficient_point"


class GenerateOrderError_CreditCardFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Creditcard payments failed"
    default_code = "Failed_Creditcard"


class Cancel_CreditCard_Payment_Failed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Failed to cancel Creditcard payment"
    default_code = "Failed_Cancel_Creditcard"

