from django.contrib import admin

# Register your models here.
from .models import User, DoctorProfile, PatientProfile, ReceptionistProfile

admin.site.register(User)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(ReceptionistProfile)

