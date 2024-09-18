from django.db import models
from django.utils import timezone
from users.models import User, DoctorProfile, PatientProfile
from treatment.models import Treatment

# Model for managing appointments
class Appointment(models.Model):
     # Choices for appointment status, which can be scheduled, completed, or canceled
    APPOINTMENT_STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="appointments_as_patient")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="appointments") 
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS_CHOICES, default='Scheduled')
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)

     # String representation of the appointment model
    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.first_name} {self.doctor.user.last_name} - {self.doctor.specialization} on {self.appointment_date}"
    
    # Custom method to check if an appointment is upcoming based on the current date and its status
    def is_upcoming(self):
        return self.appointment_date > timezone.now() and self.status == 'Scheduled'
    
# Model for managing doctor availability for appointments
class Availability(models.Model):
    # Choices for days of the week when doctors are available
    DAY_OF_WEEK_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    doctor = models.ForeignKey('users.DoctorProfile', on_delete=models.CASCADE, related_name="availabilities")
    day_of_week = models.CharField(max_length=10, choices=DAY_OF_WEEK_CHOICES)
    max_patients = models.PositiveIntegerField(default=10)

    # String representation of the availability
    def __str__(self):
        return f"{self.doctor.user.last_name}'s availability on {self.day_of_week}"
    

    # Meta class for ordering the availability records by day of the week
    class Meta:
        ordering = ['day_of_week']