from datetime import datetime

from django.db import transaction
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, Coalesce
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import PostModel, PostsLikesModel
from posts.serializers import (
    ModelPostSerializer,
    LikePostSerializer,
)


class CreatePostApiView(generics.CreateAPIView):
    serializer_class = ModelPostSerializer
    queryset = PostModel.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ListPostApiView(generics.ListAPIView):
    serializer_class = ModelPostSerializer
    queryset = PostModel.objects.all().order_by("-created_at")
    permission_classes = [AllowAny]


class LikePostApiView(APIView):
    """
    Have two use cases: for like and unlike.
        post_id: int
        action: 'like' or 'unlike'
    """

    serializer_class = LikePostSerializer

    def post(self, request):
        serializer = LikePostSerializer(data=request.data)

        if serializer.is_valid():
            post_id = serializer.validated_data.get("post_id")
            action = serializer.validated_data.get("action")

            try:
                post = PostModel.objects.get(pk=post_id)
            except PostModel.DoesNotExist:
                return Response(
                    {"error": "Post doesn't exist"}, status=status.HTTP_404_NOT_FOUND
                )

            with transaction.atomic():
                user = self.request.user
                if action == "unlike":
                    PostsLikesModel.objects.get(post=post, user=user).delete()
                else:
                    PostsLikesModel.objects.get_or_create(
                        post=post,
                        user=user,
                    )
                post.save()

            return Response(
                {
                    "id": post.id,
                    "likes": post.post_likes.count(),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostAnalyticsApiView(APIView):
    def get(self, request, post_id):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if date_from is None or date_to is None:
            return Response(
                {"errors": "date_from and date_to is required query parameters!"
                 },
                status=status.HTTP_400_BAD_REQUEST
            )

        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = datetime.strptime(date_to, "%Y-%m-%d")

        data = (
            PostsLikesModel.objects.filter(
                post_id=post_id,
                created_at__date__gte=date_from,
                created_at__date__lte=date_to,
            )
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(likes_count=Coalesce(Count("id"), 0))
            .order_by("date")
        )
        total_likes = data.aggregate(total_likes=Sum("likes_count"))["total_likes"]

        response = {
            "grouped": data,
            "all_time": total_likes
        }
        return Response(response)
