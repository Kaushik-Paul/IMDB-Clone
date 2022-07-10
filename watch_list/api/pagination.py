from rest_framework import pagination


class WatchListPagination(pagination.PageNumberPagination):
    page_size = 5
    page_query_param = 'page-size'
    page_size_query_param = 'size'
    last_page_strings = ('last', 'end',)
    max_page_size = 10


class WatchListOffSetPagination(pagination.LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchListCursorPagination(pagination.CursorPagination):
    page_size = 5
    ordering = '-created_on'
