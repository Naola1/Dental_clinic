from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User, DoctorProfile, PatientProfile
from .models import Appointment, Availability, Treatment
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, timedelta

class AppointmentViewTests(APITestCase):

    def setUp(self):
        # Create users
        self.patient = User.objects.create_user(
            username="patient1", 
            email="patient1@example.com", 
            password="password", 
            role="patient"
        )
        self.doctor = User.objects.create_user(
            username="doctor1", 
            email="doctor1@example.com", 
            password="password", 
            role="doctor"
        )
        self.receptionist = User.objects.create_user(
            username="receptionist1", 
            email="receptionist1@example.com", 
            password="password", 
            role="receptionist"
        )

        # Create profiles
        self.patient_profile = PatientProfile.objects.create(user=self.patient)
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor, specialization="General")
        

        # Create a treatment
        self.treatment = Treatment.objects.create(name="General Checkup", description="Regular checkup")

        # Create an appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient_profile,
            doctor=self.doctor_profile,
            appointment_date=date.today(),
            status="Scheduled",
            treatment=self.treatment
        )

        # Create availability
        self.availability = Availability.objects.create(
            doctor=self.doctor_profile,
            day_of_week=date.today().strftime('%A'),
            max_patients=10
        )

        

        # Get tokens
        self.patient_token = self.get_jwt_token(self.patient)
        self.doctor_token = self.get_jwt_token(self.doctor)
        self.receptionist_token = self.get_jwt_token(self.receptionist)

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_list_appointments(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        response = client.get(reverse('appointment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_appointment(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        data = {
            "patient": self.patient_profile.id,
            "doctor": self.doctor_profile.id,
            "appointment_date": (date.today() + timedelta(days=1)).isoformat(),
            "status": "Scheduled",
            "treatment": self.treatment.id
        }
        response = client.post(reverse('appointment-list'), data)
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)

    def test_update_appointment(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        data = {"status": "Completed"}
        response = client.patch(reverse('appointment-detail', kwargs={'pk': self.appointment.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Completed")

    def test_delete_appointment(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        response = client.delete(reverse('appointment-detail', kwargs={'pk': self.appointment.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_search_appointments(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        response = client.get(reverse('appointment-search'), {'query': 'patient1'})
        print(f"Search response status: {response.status_code}")
        print(f"Search response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_change_appointment_status(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        data = {"status": "Completed"}
        response = client.put(reverse('appointment-change-status', kwargs={'pk': self.appointment.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Completed")

    def test_doctor_availability(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        response = client.get(reverse('doctor-availability', kwargs={'pk': self.doctor_profile.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_doctors(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.patient_token}')

        response = client.get(reverse('booking-search-doctors'), {'specialty': 'General', 'date': date.today().strftime('%A')})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_book_appointment(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.patient_token}')

        data = {'appointment_date': (date.today() + timedelta(days=1)).strftime('%d-%m-%Y')}
        response = client.post(reverse('booking-book-appointment', kwargs={'pk': self.doctor_profile.id}), data)
        print(f"Booking response status: {response.status_code}")
        print(f"Booking response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_access(self):
        client = APIClient()

        response = client.get(reverse('appointment-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.post(reverse('appointment-list'), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)