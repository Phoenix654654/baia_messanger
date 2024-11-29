from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if response.status_code == 404:
            response.data = {
                'detail': 'К сожалению, запрашиваемый объект не найден!',
                'status': 404
            }
        elif isinstance(exc, ValidationError):
            errors = []
            for field, messages in response.data.items():
                errors.append(f"{field} - {' '.join(messages)}")
            response.data = {
                'detail': ', '.join(errors),
                'status': 400
            }
        else:
            response.data = {
                'detail': response.data.get('detail', 'An error occurred'),
                'status': response.status_code
            }
    return response
