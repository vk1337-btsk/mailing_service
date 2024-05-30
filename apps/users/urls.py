from django.urls import path

from apps.users.apps import UsersConfig
from apps.users.views import UserLoginView, UserLogoutView, UserRegisterView, ProfileView, UserPasswordResetView, \
    email_verification, toggle_activiti, ProfileUpdateView

app_name = UsersConfig.name


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='update_profile'),
    path('confirm-email/<str:token>/', email_verification, name='confirm-email'),
    path('recovery/', UserPasswordResetView.as_view(), name='recovery'),
    path('toggle_activiti/<int:pk>/', toggle_activiti, name='toggle_activiti')
]