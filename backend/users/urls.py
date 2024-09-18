from django.urls import path, include
from users.views import (
	UserRegistrationAPIView,
	UserLoginAPIView,
	UserProfileView,
    DoctorListAPIView,
    DoctorDetailAPIView,
    ChangePasswordView
    
    
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('user/register/', UserRegistrationAPIView.as_view(), name='user-register'),
	path('user/login/', UserLoginAPIView.as_view(), name='user-login'),
	path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('doctors/<int:id>/', DoctorDetailAPIView.as_view(), name='doctor-detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]