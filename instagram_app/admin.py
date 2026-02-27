from django.contrib import admin
from .models import *



admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Hashtag)
admin.site.register(Post)
admin.site.register(PostContent)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)





