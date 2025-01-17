from django.db.models import Count
from django.core.paginator import Paginator
from services.serializers import HandoutSerializer

def get_paginated_handout(request_data, context: dict, page: int, page_size: int):
    data = request_data
    total_count = data.aggregate(count=Count('id'))['count']

    paginator = Paginator(data, page_size)
    handouts = paginator.get_page(page)

    responses = {
        "totalElements": total_count,
        "totalPages": paginator.num_pages,
        "size": page_size,
        "number": page,
        "numberOfElements": len(handouts),
        "first": not handouts.has_previous(),
        "last": not handouts.has_next(),
        "empty": total_count == 0,
        "content": HandoutSerializer(handouts, many=True, context=context).data,
    }
    return responses