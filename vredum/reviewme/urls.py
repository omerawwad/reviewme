from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("items", views.items, name='items'),
    path("item/<int:item_id>", views.get_item, name='item'),
    path("highlighted", views.get_item_with_hl, name='highlighted'),
    path("review/<int:review_id>", views.review, name='review'),
    path("question/<int:question_id>", views.question, name='question'),
    path("item", views.item, name='item'),
    path("add/tag", views.add_tag, name='add_tag'),
    path("add/review", views.add_review, name='add_review'),
    path("add/question", views.add_question, name='add_question'),
    path("add/answer", views.add_answer, name='add_answer'),
    path("user/reviews", views.get_user_reviews, name='user_reviews'),
    path("user/questions", views.get_user_questions, name='user_questions'),
    path("user/answers", views.get_user_answers, name='user_answers'),
    path("like/review", views.like_review, name='like_review'),
    path("upvote/question", views.upvote_question, name='upvote_question'),
    path("like/answer", views.like_answer, name='like_answer'),
    path("edit/item", views.edit_item, name='edit_item'),
    path("delete/item", views.delete_item, name='delete_item'),
    path("delete/review", views.delete_review, name='delete_review'),
    path("delete/question", views.delete_question, name='delete_question'),
    path("delete/answer", views.delete_answer, name='delete_answer'),
]