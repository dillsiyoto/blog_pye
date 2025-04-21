from django.urls import path

from posts.views import PostsView, BasePostView


urlpatterns = [
    path(route="", view=BasePostView.as_view(), name="base"),
    path(route="post_form", 
        view=PostsView.as_view(), name="post_form"
    )
]
