from django.urls import path

from clients.views import (
    RegistrationView, 
    LoginView,
)


urlpatterns = [
    path(route="reg/", view=RegistrationView.as_view(), name="reg"),
    path(route="login/", view=LoginView.as_view(), name="login"),
]
