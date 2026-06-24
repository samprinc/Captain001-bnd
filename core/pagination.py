# core/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    # Set how many articles show up per page (matches your frontend PAGE_SIZE)
    page_size = 12 
    # Allows the frontend to request more or fewer items if needed (?page_size=24)
    page_size_query_param = 'page_size' 
    # Hard limit to prevent someone from requesting 10,000 items and crashing the server
    max_page_size = 50 

    def get_paginated_response(self, data):
        """
        We customize the response payload so React has exactly what it needs 
        to build the pagination UI without doing any math.
        """
        return Response({
            'count': self.page.paginator.count,             # Total number of articles
            'total_pages': self.page.paginator.num_pages,   # Total number of pages
            'current_page': self.page.number,               # The current page we are on
            'next': self.get_next_link(),                   # URL for the next page
            'previous': self.get_previous_link(),           # URL for the previous page
            'results': data                                 # The actual array of articles
        })