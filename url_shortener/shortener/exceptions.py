from django.http.response import JsonResponse


class JsonBadRequestResponse(JsonResponse):
    status_code = 400

class JsonMethodNotAllowedResponse(JsonResponse):
    status_code = 405

class JsonResourceNotFoundResponse(JsonResponse):
    status_code = 404

class JsonUnauthorizedResponse(JsonResponse):
    status_code = 401