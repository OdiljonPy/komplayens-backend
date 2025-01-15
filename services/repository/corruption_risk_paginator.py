from django.db.models import Count
from django.core.paginator import Paginator
from services.serializers import CorruptionRiskSerializer


def corruption_risk_paginator(query_response, page: int, page_size: int, context: dict):
    total_count = query_response.aggregate(total_count=Count('id'))['total_count']

    paginator = Paginator(query_response, page_size)
    corruption = paginator.get_page(page)

    responses = {
        "totalElements": total_count,
        "totalPages": paginator.num_pages,
        "size": page_size,
        "number": page,
        "numberOfElements": len(corruption),
        "first": not corruption.has_previous(),
        "last": not corruption.has_next(),
        "empty": total_count == 0,
        "content": CorruptionRiskSerializer(corruption, many=True, context=context).data,
    }

    return responses
