from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Treatment, TreatmentHistory
from .serializers import ( 
    TreatmentHistorySerializer, 
    TreatmentHistoryCreateSerializer,
    TreatmentHistoryReceptionistSerializer
)
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PatientTreatmentHistoryView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TreatmentHistorySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return TreatmentHistory.objects.filter(patient=user)

class DoctorTreatmentHistoryView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TreatmentHistoryCreateSerializer
        return TreatmentHistorySerializer

    def get_queryset(self):
        user = self.request.user
        return TreatmentHistory.objects.filter(doctor=user)

    def perform_create(self, serializer):
        
        serializer.save()

class DoctorTreatmentHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TreatmentHistorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TreatmentHistory.objects.filter(doctor=user)

class ReceptionistTreatmentHistoryView(generics.ListAPIView):
    serializer_class = TreatmentHistoryReceptionistSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return TreatmentHistory.objects.all()

class SearchPatientHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '')
        user = request.user

        if user.role == 'doctor':
            queryset = TreatmentHistory.objects.filter(
                Q(patient__first_name__icontains=query) | 
                Q(patient__last_name__icontains=query) |
                Q(patient__email__icontains=query),
                doctor=user
            )
            serializer = TreatmentHistorySerializer(queryset, many=True)
        elif user.role == 'receptionist':
            queryset = TreatmentHistory.objects.filter(
                Q(patient__first_name__icontains=query) | 
                Q(patient__last_name__icontains=query) |
                Q(patient__email__icontains=query)
            )
            serializer = TreatmentHistoryReceptionistSerializer(queryset, many=True)
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data)