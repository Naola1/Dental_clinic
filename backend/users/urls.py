from django.urls import path
from users.views import (
	UserRegistrationAPIView,
	UserLoginAPIView,
	UserProfileView,
    DoctorListAPIView,
    DoctorDetailAPIView
    
    
    
	#UserLogoutViewAPI,
    #VerifyEmail,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('user/register/', UserRegistrationAPIView.as_view()),
	path('user/login/', UserLoginAPIView.as_view()),
	path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('doctors/<int:id>/', DoctorDetailAPIView.as_view(), name='doctor-detail'),
	#path('user/logout/', UserLogoutViewAPI.as_view()),
    #path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
]