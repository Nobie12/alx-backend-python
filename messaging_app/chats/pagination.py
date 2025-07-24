from rest_framework.pagination import PageNumberPagination

class ChatPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # allows ?page_size=15 override
    max_page_size = 100