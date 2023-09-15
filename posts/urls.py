from django.urls import path

from posts.views import (
    CreatePostApiView,
    ListPostApiView,
    LikePostApiView,
    PostAnalyticsApiView,
)

urlpatterns = [
    path("", ListPostApiView.as_view(), name="all_posts"),
    path("create/", CreatePostApiView.as_view(), name="create"),
    path("like/", LikePostApiView.as_view(), name="like"),

    path("analitics/<int:post_id>/", PostAnalyticsApiView.as_view(), name="analysis")
]

app_name = "posts"
