from django.urls import path
from django.contrib.auth import views as auth_views

from user.views import RegistrationView

app_name = 'auth'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]