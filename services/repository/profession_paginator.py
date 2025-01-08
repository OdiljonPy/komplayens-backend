from django.core.paginator import Paginator
from django.db.models import Count
from ..serializers import ProfessionalEthicsSerializer


def profession_paginator(query_response, context: dict, page: int, page_size: int):
    total_count = query_response.aggregate(total_count=Count('id'))['total_count']

    paginator = Paginator(query_response, page_size)
    profession = paginator.get_page(page)

    responses = {
        "totalElements": total_count,
        "totalPages": paginator.num_pages,
        "size": page_size,
        "number": page,
        "numberOfElements": len(profession),
        "first": not profession.has_previous(),
        "last": not profession.has_next(),
        "empty": total_count == 0,
        "content": ProfessionalEthicsSerializer(profession, many=True, context=context).data,
    }

    return responses
