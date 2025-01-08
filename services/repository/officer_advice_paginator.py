from django.core.paginator import Paginator
from django.db.models import Count
from ..serializers import OfficerAdviceSerializer


def officer_advice_paginator(query_response, context: dict, page: int, page_size: int):
    total_count = query_response.aggregate(total_count=Count('id'))['total_count']

    paginator = Paginator(query_response, page_size)
    officer_advice = paginator.get_page(page)

    responses = {
        "totalElements": total_count,
        "totalPages": paginator.num_pages,
        "size": page_size,
        "number": page,
        "numberOfElements": len(officer_advice),
        "first": not officer_advice.has_previous(),
        "last": not officer_advice.has_next(),
        "empty": total_count == 0,
        "content": OfficerAdviceSerializer(officer_advice, many=True, context=context).data,
    }

    return responses
