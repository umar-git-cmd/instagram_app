from .models import *
from rest_framework import serializers




from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()



class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','avatar', 'bio', 'user_link', 'is_official', 'phone_number', 'birth_day', 'date_registered']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'user_link', 'is_official', 'phone_number', 'birth_day', 'date_registered']


class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username',]

class FollowListSerializer(serializers.ModelSerializer):
    follower = UserProfileNameSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower']

class FollowDetailSerializer(serializers.ModelSerializer):
    follower = UserProfileNameSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = ['follower', 'follower']


class HashtagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'hashtag_name']


class HashtagDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['hashtag_name',]



class PostListSerializer(serializers.ModelSerializer):
    hashtag = HashtagDetailSerializer(many=True, read_only=True)
    author = UserProfileNameSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'description', 'music', 'hashtag', 'created_date']


class PostDetailSerializer(serializers.ModelSerializer):
    hashtag = HashtagDetailSerializer(many=True, read_only=True)
    created_date = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    author = UserProfileNameSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['author', 'description', 'music', 'hashtag', 'created_date']


class PostContentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['id', 'file']


class PostContentDetailSerializer(serializers.ModelSerializer):
    hashtag = HashtagDetailSerializer(read_only=True)
    class Meta:
        model = PostContent
        fields = ['file','hashtag']

class DeletePostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = '__all__'



class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    user = UserProfileNameSerializer(read_only=True)
    post = PostDetailSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text', 'parent', 'created_date']


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserProfileNameSerializer(read_only=True)
    post = PostDetailSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    class Meta:
        model = Comment
        fields = ['user', 'post', 'text', 'parent', 'created_date']

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'post', 'text', 'parent', 'created_date']


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'