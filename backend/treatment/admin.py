from django.contrib import admin

# Register your models here.
from .models import TreatmentHistory, Treatment

admin.site.register(TreatmentHistory)
admin.site.register(Treatment)