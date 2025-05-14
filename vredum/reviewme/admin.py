from django.contrib import admin
from .models import AnswerLike, Review, Item, User, Tag, Link, Media, Question, Answer, ReviewLike, QuestionUpvote

# Register your models here.

admin.site.register(Review)
admin.site.register(Item)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(Media)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ReviewLike)
admin.site.register(QuestionUpvote)
admin.site.register(AnswerLike)
