from django.apps import AppConfig


class BigPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Big_Portal'

class MobileOrFullMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.mobile:
            prefix = "mobile/"
        else:
            prefix = "full/"
        response.template_name = prefix + response.template_name
        return response