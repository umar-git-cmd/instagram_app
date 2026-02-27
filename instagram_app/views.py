from .serializers import *
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

class UserProfileRegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIViewSet(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIViewSet(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class FollowListAPIViewSet(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['follower__username', 'following__username']


class FollowDetailAPIViewSet(generics.RetrieveAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowDetailSerializer
    permission_classes = [IsAuthenticated]


class HashtagListAPIViewSet(generics.ListAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagListSerializer


class HashtagDetailAPIViewSet(generics.RetrieveAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagDetailSerializer


class PostListAPIViewSet(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_date')
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hashtag']
    pagination_class = PostPagination


class PostDetailAPIViewSet(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostContentListViewAPISet(generics.ListAPIView):
    queryset = PostContent.objects.all()
    serializer_class = PostContentListSerializer


class PostContentDetailViewAPISet(generics.RetrieveAPIView):
    queryset = PostContent.objects.all()
    serializer_class = PostContentDetailSerializer


class DeletePostContentAPIViewSet(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostContentDetailSerializer


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]


class CommentListAPIViewSet(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticated]


class CommentDetailAPIViewSet(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated]


class CreateCommentAPIViewSet(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer  # исправлено: убраны скобки ()
    permission_classes = [IsAuthenticated]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer