from django.db import models
from users.models import User


class Treatment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class TreatmentHistory(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="treatment_histories")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="treatments_given")
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)
    treatment_date = models.DateField(auto_now_add=True)
    description = models.TextField()
    follow_up_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Treatment on {self.treatment_date} by Dr. {self.doctor.doctor_profile.specialization}"
    
    class Meta:
        ordering = ['-treatment_date']