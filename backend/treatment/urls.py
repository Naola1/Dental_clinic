from django.urls import path
from .views import (
    PatientTreatmentHistoryView,
    DoctorTreatmentHistoryView,
    DoctorTreatmentHistoryDetailView,
    ReceptionistTreatmentHistoryView,
    SearchPatientHistoryView,
)

urlpatterns = [
    path('patient/history/', PatientTreatmentHistoryView.as_view(), name='patient-treatment-history'),
    path('doctor/history/', DoctorTreatmentHistoryView.as_view(), name='doctor-treatment-history'),
    path('doctor/history/<int:pk>/', DoctorTreatmentHistoryDetailView.as_view(), name='doctor-treatment-history-detail'),
    path('receptionist/history/', ReceptionistTreatmentHistoryView.as_view(), name='receptionist-treatment-history'),
    path('search/', SearchPatientHistoryView.as_view(), name='search-patient-history'),
]