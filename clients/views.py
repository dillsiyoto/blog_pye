import logging

from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from clients.models import Client


logger = logging.getLogger()


class RegistrationView(View):
    """Registration controller. 
    There will be only get & post methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name="reg.html")
    
    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        email = request.POST.get("email")
        raw_password = request.POST.get("password")
        if len(raw_password) < 8:
            messages.error(
                request=request, message="Password is too short"
            )
            return render(request=request, template_name="reg.html")
        try:
            Client.objects.create(
                email=email, username=username,
                password=make_password(raw_password)
            )
            messages.info(
                request=request, message="Success Registration"
            )
            return render(
                request=request, template_name="reg.html"
            )
        except IntegrityError as ie:
            logger.error(msg="Ошибка уникальности поля", exc_info=ie)
            messages.error(
                request=request, message="Wrong login or email"
            )
            return render(request=request, template_name="reg.html")
        except Exception as e:
            logger.error(msg="Something happened", exc_info=e)
            messages.error(request=request, message=str(e))
            return render(request=request, template_name="reg.html")


class LoginView(View):
    """Login Controller."""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name="login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        password = request.POST.get("password")
        client: Client | None = authenticate(
            request=request, 
            username=username, 
            password=password,
        )
        if not client:
            messages.error(
                request=request, 
                message="Wrong username or password"
            )
            return render(request=request, template_name="login.html")
        login(request=request, user=client)
        return redirect(to="base")


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        if not is_active:
            return HttpResponse("Вы не авторизованы")
        logout(request=request)
        return redirect(to="base")


class ProvileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        if not is_active:
            return HttpResponse("Вы не авторизованы")
        logout(request=request)
        return render(request=request, template_name='profile.html')
    
