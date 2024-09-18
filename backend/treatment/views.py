from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Treatment, TreatmentHistory
from .serializers import ( 
    TreatmentHistorySerializer, 
    TreatmentHistoryCreateSerializer,
    TreatmentHistoryReceptionistSerializer,
    TreatmentSerializer,
)
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Custom pagination class to limit results to 10 per page, with the option to modify page size
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# View for patients to list their treatment history, requires JWT authentication and pagination
class PatientTreatmentHistoryView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TreatmentHistorySerializer
    pagination_class = StandardResultsSetPagination

    # Returns the treatment history for the current authenticated patient
    def get_queryset(self):
        user = self.request.user
        return TreatmentHistory.objects.filter(patient=user)

# View for doctors to list or create treatment history, uses different serializers for GET and POST methods
class DoctorTreatmentHistoryView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    # Use different serializers depending on the request method
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TreatmentHistoryCreateSerializer
        return TreatmentHistorySerializer

     # Returns the treatment history for the current authenticated doctor
    def get_queryset(self):
        user = self.request.user
        return TreatmentHistory.objects.filter(doctor=user)

    # Handle the creation of a treatment history record
    def perform_create(self, serializer):
        serializer.save()

# View for doctors to retrieve, update, or delete a specific treatment history
class DoctorTreatmentHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TreatmentHistorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Returns the treatment history record for the authenticated doctor
    def get_queryset(self):
        user = self.request.user
        return TreatmentHistory.objects.filter(doctor=user)

# View for receptionists to list all treatment histories with pagination
class ReceptionistTreatmentHistoryView(generics.ListAPIView):
    serializer_class = TreatmentHistoryReceptionistSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    # Returns all treatment history records for the receptionist role
    def get_queryset(self):
        return TreatmentHistory.objects.all()

# Custom API view to search for treatment history based on patient information, depending on the user's role
class SearchPatientHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    # Handle GET requests for searching treatment history
    def get(self, request):
        query = request.query_params.get('query', '')
        user = request.user

        # Doctors can search for their patients
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
        # If the user is not authorized, return an error
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data)

# View to list all available treatments with pagination
class TreatmentListView(generics.ListAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    pagination_class = StandardResultsSetPagination