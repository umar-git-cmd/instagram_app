from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    user_link = models.URLField(null=True, blank=True)
    is_official = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    birth_day = models.DateField(null=True, blank=True)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} {self.last_name}'


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} -> {self.following}'


class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.hashtag_name


class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField(null=True, blank=True)
    music = models.FileField(upload_to='music/', null=True, blank=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True, related_name='posts')
    tagged_users = models.ManyToManyField(UserProfile, blank=True, related_name='tagged_posts')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}  {self.description}'


class PostContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_content/')

    def __str__(self):
        return f'Content for post {self.post.id}'


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} {"liked" if self.like else "unliked"} post {self.post.id}'


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.text[:50]}'


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.user}  {self.comment.id}'


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='favorite')

    def __str__(self):
        return f'{self.user}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('favorite', 'post')

    def __str__(self):
        return f'{self.favorite.user}  {self.post.id}'


class Chat(models.Model):
    persons = models.ManyToManyField(UserProfile, related_name='chats')
    created_date = models.DateField(auto_now_add=True)



class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images_message/', null=True, blank=True)
    video = models.FileField(upload_to='videos_message/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

