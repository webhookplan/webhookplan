from drf_yasg import openapi

SUCCESSFUL = openapi.Response("Successful Request")
CREATED = openapi.Response("Successful Created")
NO_CONTENT = openapi.Response("No Content")
BAD_REQUEST = openapi.Response("Bad Request")
UNAUTHORIZED = openapi.Response("Unauthorized")
UNPROCESSABLE = openapi.Response("Unprocessable Entity")
INTERNAL_SERVER_ERROR = openapi.Response("Internal Server Error")

GET_RESPONSES = {
    200: SUCCESSFUL,
    400: BAD_REQUEST,
    401: UNAUTHORIZED,
    422: UNPROCESSABLE,
    500: INTERNAL_SERVER_ERROR,
}

POST_RESPONSES = {
    200: SUCCESSFUL,
    201: CREATED,
    400: BAD_REQUEST,
    401: UNAUTHORIZED,
    422: UNPROCESSABLE,
    500: INTERNAL_SERVER_ERROR,
}

PUT_RESPONSES = PATCH_RESPONSES = {
    200: SUCCESSFUL,
    400: BAD_REQUEST,
    401: UNAUTHORIZED,
    422: UNPROCESSABLE,
    500: INTERNAL_SERVER_ERROR,
}

DELETE_RESPONSES = {
    200: SUCCESSFUL,
    204: NO_CONTENT,
    400: BAD_REQUEST,
    401: UNAUTHORIZED,
    422: UNPROCESSABLE,
    500: INTERNAL_SERVER_ERROR,
}
