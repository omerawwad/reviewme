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
]