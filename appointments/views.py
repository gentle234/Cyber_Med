from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSerializer
from .models import Appointment

class AppointmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Save the appointment with the correct doctor/patient relationships
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Patients should see only their appointments; doctors see theirs
        if request.user.is_doctor:
            appointments = Appointment.objects.filter(doctor__user=request.user)
        else:
            appointments = Appointment.objects.filter(patient__user=request.user)

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
