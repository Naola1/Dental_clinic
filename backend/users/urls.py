from django.urls import path
from users.views import (
	UserRegistrationAPIView,
	UserLoginAPIView,
	UserViewAPI,
	#UserLogoutViewAPI,
    VerifyEmail,
)


urlpatterns = [
	path('user/register/', UserRegistrationAPIView.as_view()),
	path('user/login/', UserLoginAPIView.as_view()),
	path('user/', UserViewAPI.as_view()),
	#path('user/logout/', UserLogoutViewAPI.as_view()),
     path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
]