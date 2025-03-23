from django.urls import path
from users import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()



urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
