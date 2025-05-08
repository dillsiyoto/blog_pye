from django.urls import path

from clients.views import (
    RegistrationView, 
    LoginView,
    LogoutView,
    ProfileView,
    EditProfileView
)


urlpatterns = [
    path(route="reg/", view=RegistrationView.as_view(), name="reg"),
    path(route="login/", view=LoginView.as_view(), name="login"),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
    path(route="profile/", view=ProfileView.as_view(), name="profile"),
    path(route="edit_profile/", view=EditProfileView.as_view(), name="edit_profile")
]
