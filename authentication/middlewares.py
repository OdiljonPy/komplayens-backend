from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.urls import reverse
from utils.check_token import validate_token


class UserAuthMiddleware(MiddlewareMixin):
    def process_request(self, request, *view_args, **view_kwargs):
        include_urls = [reverse('user_detail'),
                        reverse('create_officer_advice'), reverse('list_officer_advice')
                        ]
        pk = view_kwargs.get('pk')
        # if pk is not None:
        #     include_urls.append(reverse(viewname='', kwargs={'pk': pk}))

        if request.path not in include_urls:
            return
        payload = validate_token(request.headers.get('Authorization'))
        if not payload:
            return JsonResponse(data={'result': '', 'error': 'Unauthorized access', 'ok': False}, status=401)
        return
