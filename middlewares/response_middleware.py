from django.http import JsonResponse, HttpResponseServerError, HttpResponse

class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        try:
            response = self.get_response(request)
            jsonData = {
                "code": HttpResponse.status_code,
                "message": "success",
                "data": response
            }
            return JsonResponse(jsonData)
        except:
            return HttpResponseServerError("服务器内部错误")
