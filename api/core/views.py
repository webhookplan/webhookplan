from rest_framework.views import APIView
from rest_framework import response, status


class Ping(APIView):
    def get(self, *args, **kwargs):
        return response.Response(data={"details": "ok"}, status=status.HTTP_200_OK)
