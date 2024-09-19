from django.db import models
from users.models import User

# Model for defining different types of treatments
class Treatment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    # String representation of the Treatment model, returns the treatment name
    def __str__(self):
        return self.name

# Model to track treatment history for patients
class TreatmentHistory(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="treatment_histories")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="treatments_given")
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True)
    treatment_date = models.DateField(auto_now_add=True)
    description = models.TextField()
    follow_up_date = models.DateField(blank=True, null=True)

    # String representation of the TreatmentHistory model
    def __str__(self):
        return f"Treatment on {self.treatment_date} by Dr. {self.doctor.first_name}"
    
    # Meta class to order treatment histories by treatment date in descending order
    class Meta:
        ordering = ['-treatment_date']