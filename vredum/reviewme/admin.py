from django.contrib import admin
from .models import Review, Item, User, Tag, Link, Media, Question, Answer
from django.contrib.auth.models import User as AuthUser

# Register your models here.

admin.site.register(Review)
admin.site.register(Item)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(Media)
admin.site.register(Question)
admin.site.register(Answer)
