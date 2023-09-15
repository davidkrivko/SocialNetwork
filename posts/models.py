from django.db import models

from posts.file_path import custom_upload_path


class PostModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField(
        upload_to=custom_upload_path,
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        "users.UserModel",
        on_delete=models.CASCADE,
        related_name="posts"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostsLikesModel(models.Model):
    post = models.ForeignKey(
        "PostModel",
        on_delete=models.CASCADE,
        related_name="post_likes",
    )
    user = models.ForeignKey(
        "users.UserModel",
        on_delete=models.CASCADE,
        related_name="like_posts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
