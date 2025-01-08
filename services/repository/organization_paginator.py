from django.core.paginator import Paginator
from services.serializers import OrganizationSerializer
from django.db.models import Count

def get_paginated_organizations(context: dict, request_data, page, page_size):
    organization_query = request_data
    total_count = organization_query.aggregate(count=Count('id'))['count']

    paginator = Paginator(organization_query, page_size)
    organizations = paginator.get_page(page)

    responses = {
        "totalElements": total_count,
        "totalPages": paginator.num_pages,
        "size": page_size,
        "number": page,
        "numberOfElements": len(organizations),
        "first": not organizations.has_previous(),
        "last": not organizations.has_next(),
        "empty": total_count == 0,
        "content": OrganizationSerializer(organizations, many=True, context=context).data,
    }

    return responses
