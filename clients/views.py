import logging
import os

from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from clients.models import Client
from clients.utils import send_email


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


class ProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        if not is_active:
            return redirect(to = 'login')
        return render(request=request, template_name='profile.html')
    
    
class EditProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        if not is_active:
            return redirect(to = 'login')
        return render(request=request, template_name='edit_profile.html')
    
    def post(self, request: HttpRequest) -> HttpResponse:
        delete_profile = request.POST.get('delete_profile')
        if delete_profile == 'true':
            user.delete()
            return redirect('login')
        
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.birthday = request.POST.get('birthday')  
        user.gender = request.POST.get('gender')      
        user.save()
        return redirect('profile')
    
class ActivationView(View):
    def get(
        self, request: HttpRequest, username: str, code: str
    ) -> HttpResponse:
        client = Client.objects.filter(
            username=username,
            activation_code=code
        ).first()
        if not client:
            return HttpResponse(content="<h1>Ты кто?</h1>")
        client.is_active = True
        client.save(update_fields=["is_active"])
        return redirect(to="login")
    

class ResetPassword(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name='email_for_reset.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.POST.get('email')
        client = Client.objects.filter(
            email = email
        ).first()
        username = client.username
        new_password = os.urandom(6).hex()
        if not client:
            return HttpResponse(content="<h1>Авторизуйтесь</h1>")
        send_email(
            template="reset_password.html", 
            context={
                "username": username, 
                "new_password": new_password},
            to=email, title="Confirm your account"
        )
        client.password = make_password(new_password)
        client.save(update_fields=["password"])
        return redirect(to="login")
