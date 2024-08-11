from django.http import JsonResponse, HttpResponseServerError, HttpResponse


class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            jsonData = {
                "code": HttpResponse.status_code,
                "success": True,
                "data": response,
            }
            return JsonResponse(jsonData)
        except Exception as err:
            error_message = str(err)
            return HttpResponseServerError(content=error_message)
