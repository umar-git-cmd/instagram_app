from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'post/like', PostLikeViewSet, basename='post-like')
router.register(r'comment/like', CommentLikeViewSet, basename='comment-like')
router.register(r'favorite', FavoriteViewSet, basename='favorite')
router.register(r'favorite/item', FavoriteItemViewSet, basename='favorite-item')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/content', PostContentListViewAPISet.as_view(), name='post-content-list'),
    path('posts/content/<int:pk>/', PostContentDetailViewAPISet.as_view(), name='post-content-detail'),
    path('posts/', PostListAPIViewSet.as_view(), name='post-list'),
    path('posts/<int:pk>', PostDetailAPIViewSet.as_view(), name='post-detail'),
    path('posts/delete', DeletePostContentAPIViewSet.as_view(), name='delete-posts'),
    path('comments/', CommentListAPIViewSet.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailAPIViewSet.as_view(), name='comment-detail'),
    path('comments/create/', CreateCommentAPIViewSet.as_view(), name='create-comment'),
    path('users/', UserProfileListAPIViewSet.as_view(), name='user-list'),
    path('users/<int:pk>/', UserProfileDetailAPIViewSet.as_view(), name='user-detail'),
    path('follows/', FollowListAPIViewSet.as_view(), name='follow-list'),
    path('follows/<int:pk>', FollowDetailAPIViewSet.as_view(), name='follow-detail'),
    path('hashtag/', HashtagListAPIViewSet.as_view(), name='hashtag-list'),
    path('hashtag/<int:pk>/', HashtagDetailAPIViewSet.as_view(), name='hashtag-detail'),
    path('register/', UserProfileRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]