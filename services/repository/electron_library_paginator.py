from urllib import request

from django.core.paginator import Paginator
from django.db.models import Count
from services.serializers import ElectronLibrarySerializer

def get_paginated_e_library(request_data, context: dict, page, page_size):
    data = request_data
    total_count = data.aggregate(count=Count('id'))['count']

    paginator = Paginator(data, page_size)
    e_libraries = paginator.get_page(page)

    responses = {
        "totalElements": total_count,
        "totalPages": paginator.num_pages,
        "size": page_size,
        "number": page,
        "numberOfElements": len(e_libraries),
        "first": not e_libraries.has_previous(),
        "last": not e_libraries.has_next(),
        "empty": total_count == 0,
        "content": ElectronLibrarySerializer(e_libraries, many=True, context=context).data,
    }

    return responses