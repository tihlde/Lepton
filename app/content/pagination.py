from rest_framework.pagination import PageNumberPagination

class TwentyFivePagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'None'