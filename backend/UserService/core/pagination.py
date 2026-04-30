from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination
from rest_framework.response import Response

from core.response import FormatResponse
from core.utils import format_response


class LimitOffsetPaginationFormated(LimitOffsetPagination):
    base_response = FormatResponse

    def get_paginated_response(self, data):
        response_format = getattr(self, "base_response", Response)
        return response_format({
            'count': self.count,
            'results': data
        })


class PageNumberPaginationFormatted(PageNumberPagination):
    DEFAULT_PAGE_SIZE = 10
    DEFAULT_MAX_PAGE_SIZE = 10000

    page_size = DEFAULT_PAGE_SIZE
    max_page_size = DEFAULT_MAX_PAGE_SIZE
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(format_response(data={
            'pagination': {
                'page_size': self.get_page_size(self.request),
                'total_records': self.page.paginator.count,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'next_page': self.get_next_link(),
                'previous_page': self.get_previous_link(),
            },
            'results': data,
        }))


class LimitOffsetPaginationFormatted(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10000
    limit_query_param = 'limit'
    offset_query_param = 'offset'

    def get_paginated_response(self, data):
        limit = self.get_limit(self.request)
        offset = self.get_offset(self.request)
        total = self.count

        next_offset = offset + limit if offset + limit < total else None

        return Response(format_response(data={
            'pagination': {
                'limit': limit,
                'offset': offset,
                'total_records': total,
                'has_more': next_offset is not None,
                'next_offset': next_offset,
            },
            'results': data,
        }))


class CursorPaginationFormatted(CursorPagination):
    page_size = 20
    ordering = '-created_at'

    def get_paginated_response(self, data):
        return Response(format_response(data={
            'pagination': {
                'next_cursor': self.get_next_link(),
                'previous_cursor': self.get_previous_link(),
            },
            'results': data,
        }))


class LimitOffsetPaginationWithTotal(LimitOffsetPagination):
    def __init__(self):
        super().__init__()
        self.total = None

    def set_total(self, total):
        self.total = total

    def get_paginated_response(self, data):
        response_data = {
            'count': self.count,
            'results': data
        }
        if self.total is not None:
            response_data['total'] = self.total

        return Response(format_response(data=response_data))
