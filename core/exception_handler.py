from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler

from core.exceptions import (
    BusinessRuleError,
    PermissionDeniedError,
    ConflictError,
    NotFoundError,
)

def custom_exception_handler(exc, context):

    if isinstance(exc, BusinessRuleError):
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(exc, PermissionDeniedError):
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_403_FORBIDDEN
        )

    if isinstance(exc, NotFoundError):
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, ConflictError):
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_409_CONFLICT
        )

    return exception_handler(exc, context)
