from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ChatPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # allows ?page_size=15 override
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,     # ✅ REQUIRED BY THE CHECK
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })