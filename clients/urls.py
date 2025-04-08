from django.urls import path

from clients.views import (
    BasePageView, 
    RegistrationView, 
    LoginView,
)


urlpatterns = [
    path(route="", view=BasePageView.as_view(), name="base"),
    path(route="reg/", view=RegistrationView.as_view(), name="reg"),
    path(route="login/", view=LoginView.as_view(), name="login"),
]
