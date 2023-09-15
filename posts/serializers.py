from rest_framework import serializers

from posts.models import PostModel


class ModelPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = PostModel
        fields = ("id", "title", "content", "photo", "likes")
        read_only = ("likes",)

    def get_likes(self, obj):
        return obj.post_likes.count()

    def create(self, validated_data):
        photo = validated_data.pop("photo")
        post = super().create(validated_data)
        post.photo = photo
        post.save()

        return post


class LikePostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=["like", "unlike"])
