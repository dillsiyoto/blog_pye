import logging

from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from posts.models import Posts, Images, Categories


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
        categories = Categories.objects.all()
        if not categories:
            return HttpResponse(
                content="<h1>Something went wrong</h1>"
            )
        if not is_active:
            return redirect(to="login")
        return render(
            request=request, template_name="post_form.html",
            context={"categories": categories}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        images = request.FILES.getlist("images")
        post = Posts.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
        post.categories.set(request.POST.getlist("categories"))
        imgs = [Images(image=img, post=post) for img in images]
        # for img in images:
        #     Images.objects.create(
        #         image=img,
        #         post=post
        #     )
        Images.objects.bulk_create(imgs)
        return redirect(to="base")
        

    def put(self, request: HttpRequest) -> HttpResponse:
        pass

    def patch(self, request: HttpRequest) -> HttpResponse:
        pass

    def delete(self, request: HttpRequest) -> HttpResponse:
        pass
