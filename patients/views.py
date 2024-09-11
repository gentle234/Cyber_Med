from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientSerializer

class PatientProfileView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Patient profile created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
