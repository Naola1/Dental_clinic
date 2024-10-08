from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, AvailabilityViewSet, DoctorViewSet, AppointmentBookingViewSet

# Create a default router to automatically generate URL routes for viewsets
router = DefaultRouter()

router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'availabilities', AvailabilityViewSet, basename='availability')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'bookings', AppointmentBookingViewSet, basename='booking')

# URL patterns
urlpatterns = [
     # Include all the routes generated by the router
    path('', include(router.urls)), 
    path('appointments/search/', AppointmentViewSet.as_view({'get': 'search_appointments'}), name='appointment-search'),
]
