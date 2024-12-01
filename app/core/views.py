"""
Api Views for core app functionalities.
"""

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from utils.logging import print_error


def health_check(request):
    """API Health Check."""

    payload = {"status": 200, "message": "Systems operational."}
    return JsonResponse(payload, status=200)


def custom404(request, exception):
    """Custom 404 response."""

    return Response(
        {"status_code": 404, "message": "Page not found."},
        status=status.HTTP_404_NOT_FOUND,
    )


def api_exception_handler(exc, context):
    """
    Custom exception handler for api.
    Linked in settings.py as REST_FRAMEWORK -> "EXCEPTION_HANDLER".

    Ref: https://www.django-rest-framework.org/api-guide/exceptions/
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code
    else:
        print_error()
        response = Response(
            {"status_code": 400, "message": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return response
