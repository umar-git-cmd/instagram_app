from .models import *
from modeltranslation.translator import TranslationOptions,register

@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('bio',)

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('text',)

