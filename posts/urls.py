from django.urls import path

from posts.views import (
    PostsView, BasePostView, ShowDeletePostView
)


urlpatterns = [
    path(route="", view=BasePostView.as_view(), name="base"),
    path(route="post_form", 
        view=PostsView.as_view(), name="post_form"
    ),
    path(route="show_post/<int:pk>", 
        view=ShowDeletePostView.as_view(), name="pk_post"
    )
]
