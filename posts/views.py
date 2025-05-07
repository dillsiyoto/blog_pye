import logging
from typing import Literal

from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError

from posts.models import Posts, Images, Categories, LikesDislikes


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
        Images.objects.bulk_create(imgs)
        # for img in images:
        #     Images.objects.create(
        #         image=img,
        #         post=post
        #     )
        return redirect(to="base")


class ShowDeletePostView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            post = None
        author = False
        if request.user == post.user:
            author = True
        return render(
            request=request, template_name="pk_post.html",
            context={
                "post": post,
                "author": author
            }
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            pass
        if request.user != post.user:
            return HttpResponse(
                "<h1>У тебя здесь нет власти</h1>"
            )
        post.delete()
        return redirect(to="base")


class LikesView(View):
    def post(
        self, request: HttpRequest, 
        pk: int, action: Literal["like", "dislike"] 
    ):
        client = request.user # проверяем активен ли пользовтель
        if not client.is_active:
            return HttpResponse("Вы не вошли") # если не активен, то сообщаем
        try:
            post = Posts.objects.get(pk=pk) # пробуем найти пост по айди
        except Posts.DoesNotExist:
            return HttpResponse("Пост не найден") # если пост не найден, то сообщаем
        
        vote = LikesDislikes.objects.filter(user=client, post=post).first() # ищем оставлял ли лайк юзер
        if vote: # если оставлял
            if action == 'like': # если оставлял лайк
                if vote.action == 'dislike': # и меняет на дизлайк
                    post.likes -= 1 # убираем лайк
                    post.dislikes += 1 # ставим дизлайк

            elif action == 'diclike': # если оставлял дизлайк
                if vote.action == 'like': # и меняет на лайк
                    post.dislikes -= 1 # убираем дизлайк
                    post.likes += 1 # ставим лайк
            vote.save() # сохраняем
        else: # если не оставлял
            if vote.action == 'like': # и хочет оставить лайк
                post.likes += 1 # ставим лайк
            elif action == 'dislike': # если хочет оставить дизлайк
                post.dislikes += 1 # ставим дизлайк
            LikesDislikes.objects.create(user=client, post=post, action=action) # записываем в базу
        post.save(update_fields=["likes", "dislikes"]) # сохраняем
        return JsonResponse({
            "likes": post.likes,
            "dislikes": post.dislikes
        })
            