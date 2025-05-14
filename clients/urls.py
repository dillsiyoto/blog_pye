from django.urls import path

from clients.views import (
    RegistrationView, 
    LoginView,
    LogoutView,
    ProfileView,
    EditProfileView,
    ActivationView,
    ResetPassword
)


urlpatterns = [
    path(route="reg/", view=RegistrationView.as_view(), name="reg"),
    path(route="login/", view=LoginView.as_view(), name="login"),
    path(route="logout/", view=LogoutView.as_view(), name="logout"),
    path(route="profile/", view=ProfileView.as_view(), name="profile"),
    path(route="edit_profile/", view=EditProfileView.as_view(), name="edit_profile"),
    path(
        route="activation/<str:username>/<str:code>", 
        view=ActivationView.as_view(), name="activate"
    ),
    path(route="reset/", view=ResetPassword.as_view(), name="resetpassword")
]
