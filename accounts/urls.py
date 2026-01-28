from django.urls import path, include
from django.contrib.auth.views import LoginView
from .forms import UserLoginForm
from . import views


urlpatterns = [
    path('login/', LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.edit_profile, name='profile'),
    path('', include('django.contrib.auth.urls')),
    path('<str:lang>/', views.SwitchLangView.as_view(), name='switch-lang')
]