from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from .models import Treatment, TreatmentHistory
from rest_framework_simplejwt.tokens import RefreshToken

# Test class for TreatmentHistory views
class TreatmentHistoryViewTests(APITestCase):

    def setUp(self):
        # Create a patient user with the role of 'patient'
        self.patient = User.objects.create_user(
            username="patient1", 
            email="patient1@example.com", 
            password="password", 
            role="patient"
        )
        # Create a doctor user with the role of 'doctor'
        self.doctor = User.objects.create_user(
            username="doctor1", 
            email="doctor1@example.com", 
            password="password", 
            role="doctor"
        )
        # Create a receptionist user with the role of 'receptionist'
        self.receptionist = User.objects.create_user(
            username="receptionist1", 
            email="receptionist1@example.com", 
            password="password", 
            role="receptionist"
        )

        # Create a Treatment instance with basic info
        self.treatment = Treatment.objects.create(name="Tooth Cleaning", description="Regular cleaning")

        # Create a TreatmentHistory instance associating the patient, doctor, and treatment
        self.treatment_history = TreatmentHistory.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            treatment=self.treatment,
            description="Cleaning completed"
        )

        # Generate JWT tokens for the patient, doctor, and receptionist for authentication in tests
        self.patient_token = self.get_jwt_token(self.patient)
        self.doctor_token = self.get_jwt_token(self.doctor)
        self.receptionist_token = self.get_jwt_token(self.receptionist)

    # Helper method to generate JWT token for a user
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
     # Test that a patient can view their treatment history
    def test_patient_treatment_history(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.patient_token}')

        response = client.get(reverse('patient-treatment-history'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['description'], "Cleaning completed")

    # Test that a doctor can view treatment histories
    def test_doctor_treatment_history(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        response = client.get(reverse('doctor-treatment-history'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['description'], "Cleaning completed")

    # Test that a doctor can create a new treatment history record
    def test_doctor_can_create_treatment_history(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')
        # Data for the new treatment history
        data = {
            "patient": self.patient.id,
            "treatment": self.treatment.id,
            "description": "New treatment for cavities"
        }
        response = client.post(reverse('doctor-treatment-history'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TreatmentHistory.objects.count(), 2)
        
    # Test that a receptionist can view all treatment histories
    def test_receptionist_can_view_all_treatment_histories(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.receptionist_token}')

        response = client.get(reverse('receptionist-treatment-history'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    # Test that a doctor can search for a patient's treatment history by query
    def test_search_patient_history_as_doctor(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        response = client.get(reverse('search-patient-history'), {'query': 'patient1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test that unauthorized users cannot access treatment histories
    def test_unauthorized_access(self):
        client = APIClient()

        response = client.get(reverse('patient-treatment-history'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.get(reverse('doctor-treatment-history'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)