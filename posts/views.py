import logging

from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from posts.models import Posts, Images


logger = logging.getLogger()


class BasePostView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        posts: QuerySet[Posts] = Posts.objects.all()
        return render(
            request=request, template_name="posts.html", 
            context={
                "posts": posts,
                "user": is_active
            }
        )


class PostsView(View):
    """Posts controller with all methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        if not is_active:
            return redirect(to="login")
        return render(
            request=request, template_name="post_form.html"
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        pass

    def put(self, request: HttpRequest) -> HttpResponse:
        pass

    def patch(self, request: HttpRequest) -> HttpResponse:
        pass

    def delete(self, request: HttpRequest) -> HttpResponse:
        pass
