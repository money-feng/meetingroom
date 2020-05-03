from django.utils.deprecation import MiddlewareMixin

class CorsMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = 'Content-Type'

        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = "*"
        return response