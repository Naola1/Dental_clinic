# DentalCare Management System

**Making it easy for you to book appointments and keep track of your dental health.**

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

DentalCare Management System is designed to facilitate appointment scheduling, patient record management, and efficient clinic operations. The system is flexible for use by clinics of varying sizes and helps streamline communication between patients, doctors, and staff.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: React (TypeScript)
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL
- **Deployment**: Render

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/dentalcare-management.git
   cd dentalcare-management
   ```
2. Create a virtual environment:
   python3 -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate

3. pip install -r requirements.txt
   pip install -r requirements.txt

4. Set up environment variables (.env file) for JWT_SECRET, MySQL connection, and others.
5. Run migrations:
   python manage.py migrate

6. Start the server:
   python manage.py runserver

API Documentation
You can view the auto-generated API documentation using drf-yasg. After starting the server, navigate to:
http://localhost:8000/swagger/

Authentication APIs
User Registration: /api/users/register/

Registers a new patient by default.
Fields: email, username, password

User Login: /api/users/login/

Logs in a user using email and password.
Returns JWT access token.

User APIs
User Profile: /api/users/profile/
GET: Retrieves the logged-in user's profile.
PUT: Updates profile information based on user role.
DELETE: Deletes the user account.
Treatment APIs
Doctor Treatment History: /api/treatments/doctor-history/

GET: Retrieves the treatment history for a doctor.
POST: Creates new treatment history (Doctor only).
Patient Treatment History: /api/treatments/patient-history/

GET: Retrieves treatment history for a logged-in patient.
Search API
Search Patient History: /api/treatments/search-history/
GET: Search patient's treatment history (Doctor/Receptionist).
Usage
To test the application:

1. Create a User: Register a patient through /api/users/register/.
2. Login: Use the credentials to log in and receive an authentication token.
3. Access User Profile: Use the token to access the user's profile and manage treatments.

Project Structure
├── backend/
│ ├── appointments/ # Handles appointment scheduling and doctor availability
│ ├── Users/ # Manages user roles, profiles (patient, doctor, receptionist)
│ ├── treatments/ # Manages treatment types, history
│ ├── notifications/ # Manages notifications for users
│ └── manage.py # Django management file
├── frontend/ # React app for the user interface
│ ├── src/
│ └── package.json
├── .env # Environment variables for database and JWT settings
├── Dockerfile # Docker setup for containerization
├── requirements.txt # Python dependencies
└── README.md # This file

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new feature branch.
Commit your changes.
Submit a pull request.
