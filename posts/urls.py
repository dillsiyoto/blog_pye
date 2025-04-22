from django.urls import path

from posts.views import PostsView, BasePostView, EditPostView


urlpatterns = [
    path(route="", view=BasePostView.as_view(), name="base"),
    path(route="post_form", 
        view=PostsView.as_view(), name="post_form"
    ),
    path(route="post/<int:pk>", 
        view=EditPostView.as_view(), name="pk_post"
    )
]
