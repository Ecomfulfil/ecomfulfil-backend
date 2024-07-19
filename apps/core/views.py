from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

class HealthCheckView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

    def get(self, request):
        data = {
            "message": "Service is up and running!"
        }
        return Response(data, status=status.HTTP_200_OK)