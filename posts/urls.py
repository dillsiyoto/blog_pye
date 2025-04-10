from django.urls import path

from posts.views import PostsView


urlpatterns = [
    path(route="", view=PostsView.as_view(), name="posts")
]
