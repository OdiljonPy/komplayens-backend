from services.serializers import AnnouncementSerializer
from django.core.paginator import Paginator
from django.db.models import Count

def get_paginated_announcement(context: dict, request_data, page, page_size):
    announcement_query = request_data
    total_count = announcement_query.aggregate(count=Count('id'))['count']

    paginator = Paginator(announcement_query, page_size)
    announcements = paginator.get_page(page)

    responses = {
        "totalElements": total_count,
        "totalPages": paginator.num_pages,
        "size": page_size,
        "number": page,
        "numberOfElements": len(announcements),
        "first": not announcements.has_previous(),
        "last": not announcements.has_next(),
        "empty": total_count == 0,
        "content": AnnouncementSerializer(announcements, many=True, context=context).data,
    }

    return responses
