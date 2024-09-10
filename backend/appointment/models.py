from django.db import models
from django.utils import timezone
from users.models import User, DoctorProfile, PatientProfile
from treatment.models import Treatment

class Appointment(models.Model):
    APPOINTMENT_STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="appointments_as_patient")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="appointments") 
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS_CHOICES, default='Scheduled')
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.first_name} {self.doctor.user.last_name} - {self.doctor.specialization} on {self.appointment_date}"
    
    def is_upcoming(self):
        return self.appointment_date > timezone.now() and self.status == 'Scheduled'
    

class Availability(models.Model):
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

    def __str__(self):
        return f"{self.doctor.user.last_name}'s availability on {self.day_of_week}"
    
    class Meta:
        ordering = ['day_of_week']