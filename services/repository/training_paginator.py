from django.core.paginator import Paginator
from django.db.models import Count
from ..serializers import TrainingSerializer


def training_paginator(query_response, context: dict, page: int, page_size: int):
    total_count = query_response.aggregate(total_count=Count('id'))['total_count']

    paginator = Paginator(query_response, page_size)
    training = paginator.get_page(page)

    responses = {
        "totalElements": total_count,
        "totalPages": paginator.num_pages,
        "size": page_size,
        "number": page,
        "numberOfElements": len(training),
        "first": not training.has_previous(),
        "last": not training.has_next(),
        "empty": total_count == 0,
        "content": TrainingSerializer(training, many=True, context=context).data,
    }

    return responses
