from django.db.models import DateTimeField
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'items': data,
        })


class DateTimeWithoutTZField(DateTimeField):
    """ Use when creating DateTimeField without time zone """

    def db_type(self, connection):
        return 'timestamp without time zone'
