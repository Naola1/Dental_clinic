from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from users.models import PatientProfile, DoctorProfile, ReceptionistProfile

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        # Creating a user for authentication
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'username': 'johndoe',  # Add the username
            'password': 'password123'
        }
        self.user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],  # Add the username
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            password=self.user_data['password']
        )
        self.patient_profile = PatientProfile.objects.create(user=self.user)

        # Create a doctor user
        self.doctor_data = {
            'first_name': 'Dr. Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'username': 'drjane',  # Add the username
            'password': 'password123',
            'role': 'doctor'  # Assuming you have a role field for doctors
        }
        self.doctor = User.objects.create_user(
            email=self.doctor_data['email'],
            username=self.doctor_data['username'],  # Add the username
            first_name=self.doctor_data['first_name'],
            last_name=self.doctor_data['last_name'],
            password=self.doctor_data['password'],
            role=self.doctor_data['role']
        )
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor)

        # Create a receptionist user
        self.receptionist_data = {
            'first_name': 'Sarah',
            'last_name': 'Connor',
            'email': 'sarah.connor@example.com',
            'username': 'sarahconnor',  # Add the username
            'password': 'password123',
            'role': 'receptionist'
        }
        self.receptionist = User.objects.create_user(
            email=self.receptionist_data['email'],
            username=self.receptionist_data['username'],  # Add the username
            first_name=self.receptionist_data['first_name'],
            last_name=self.receptionist_data['last_name'],
            password=self.receptionist_data['password'],
            role=self.receptionist_data['role']
        )
        self.receptionist_profile = ReceptionistProfile.objects.create(user=self.receptionist)

        # Authenticate user for the test cases
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        """Test user registration API"""
        registration_data = {
            'first_name': 'Alice',
            'last_name': 'Brown',
            'email': 'alice.brown@example.com',
            'username': 'alicebrown',  # Add the username
            'password': 'password123'
        }
        response = self.client.post(reverse('user-register'), registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        """Test user login API"""
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(reverse('user-login'), login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_get(self):
        """Test retrieving the user profile"""
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_user_profile_update(self):
        """Test updating the user profile"""
        update_data = {
            'first_name': 'John Updated',
            'last_name': 'Doe Updated'
        }
        response = self.client.put(reverse('user-profile'), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, update_data['first_name'])
        self.assertEqual(self.user.last_name, update_data['last_name'])

    def test_change_password(self):
        """Test changing the user password"""
        change_password_data = {
            'old_password': 'password123',
            'new_password': 'newpassword123'
        }
        response = self.client.post(reverse('change_password'), change_password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_incorrect_old_password(self):
        """Test changing the password with incorrect old password"""
        change_password_data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123'
        }
        response = self.client.post(reverse('change_password'), change_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doctor_list(self):
        """Test retrieving the list of doctors"""
        response = self.client.get(reverse('doctor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_different_user_roles(self):
        """Test user roles - doctor"""
        self.client.force_authenticate(user=self.doctor)
        response = self.client.get(reverse('doctor-detail', kwargs={'pk': self.doctor.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.doctor.username)

        self.client.force_authenticate(user=self.receptionist)
        response = self.client.get(reverse('receptionist-detail', kwargs={'pk': self.receptionist.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.receptionist.username)