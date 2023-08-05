"""
==============
API Middleware
==============

"""
from django.http import JsonResponse
from django.conf import settings
from ua_parser import user_agent_parser
from rest_framework import status
from authorized import api_check
from authorized import api_token
from authorized import api_utils


class APIAuthRequestMiddleware:
    """
    Middleware that will evaluate if the incoming request is
    authorized to comunicate with the current application.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.custom_response = None
        self.error_data = None
        self.error_status = status.HTTP_400_BAD_REQUEST

    def __call__(self, request):
        response = self.get_response(request)
        # Variables missing settings.APP_NAME or os.environ.get('APP_KEY')
        if not api_utils.has_key() or not api_utils.has_name():
            error_data = {'message': 'APP_NAME or APP_KEY missing.'} if settings.DEBUG else {'message': 'Application has not being set properly.'}
            return JsonResponse(error_data, status=status.HTTP_400_BAD_REQUEST)
        # Before returning response headers can be appended to the response object, below this comment is an appropiate place.

        if 'authorized' not in request.path.split('/'):
            response['Application-Token'] = api_token.generate()
        return response

    def process_header(self, request_headers):
        """
        Process 'Application-Token' header provided in the request, search the application name in the database table and will create the response accordingly.
        """
        token = api_check.header_token(request_headers)
        if token['has_token']:
            token_verified = api_token.verify(token['token'])
            if token_verified['is_valid']:
                app = api_check.is_application_authorized(token_verified['app_name'])
                if app['is_authorized']:
                    return True
                else:
                    self.error_data = {'message': app['message']}
                    self.error_status = status.HTTP_401_UNAUTHORIZED
                    return False
            else:
                self.error_data = {'message': token_verified['message']}
                return False
        else:
            self.error_data = {'message': token['message']}
            return False

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'authorized' in request.path.split('/'):
            return view_func(request, *view_args, **view_kwargs)

        # when in debug mode, the middleware will skip incoming requests that come from sources like browsers or Postman.
        if settings.DEBUG:
            parsed_agent = user_agent_parser.Parse(request.META['HTTP_USER_AGENT'])
            if 'Postman' or 'Mozilla' or 'Chrome' or 'insomnia' in parsed_agent['string']:
                return view_func(request, *view_args, **view_kwargs)

        # process header token
        if self.process_header(request.META):
            return view_func(request, *view_args, **view_kwargs)
        else:
            return JsonResponse(self.error_data, status=self.error_status)
