import functools
import logging
import traceback

from django.db import transaction
from django.http import JsonResponse
from django.views.generic import View

logger = logging.getLogger(__name__)

JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


def ret(json_object, status=200):
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def error_response(exception):
    res = {'errorMessage': str(exception),
           'traceback': traceback.format_exc()}
    return ret(res, status=400)


def base_view(fn):
    """Decorator for all views, process exception"""
    @functools.wraps(fn)
    def inner(request, *args, **kwargs):

        try:
            with transaction.atomic():
                return fn(request, *args, **kwargs)
        except Exception as e:
            view = request.resolver_match.view_name
            path = request.path
            method = request.method
            if request.user.is_authenticated:
                username = request.user.full_name()
            else:
                username = 'AnonymousUser'
            logger.error(f'errorMsg: {str(e)} viewClass: {view} path: {path} httpMethod: {method} user: {username}'
                         f'\ntraceback: {traceback.format_exc()}')
            return error_response(e)
    return inner


class BaseView(View):
    """ Base class for all views, process exception"""
    def dispatch(self, request, *args, **kwargs):
        view = request.resolver_match.view_name
        path = request.path
        method = request.method

        if request.user.is_authenticated:
            username = request.user.get_full_name()
        else:
            username = 'AnonymousUser'

        try:
            response = super(BaseView, self).dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f'errorMsg: {str(e)} viewClass: {view} path: {path} httpMethod: {method} user: {username}'
                         f'\ntraceback: {traceback.format_exc()}')
            return self._response({'msg': str(e),
                                   'success': False,
                                   'traceback': traceback.format_exc()}, status=500)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params=JSON_DUMPS_PARAMS
        )