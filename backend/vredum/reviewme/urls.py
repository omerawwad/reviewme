from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.index, name='index'),
    path("reviews", views.reviews, name='reviews'),
    path("tag/<str:tag_name>", views.get_items_by_tag, name='get_items_by_tag'),
    path("search", views.search_items, name='search_items'),
    path("item/<int:item_id>", views.get_item, name='item'),
    path("review/<int:review_id>", views.review, name='review'),
    path("question/<int:question_id>", views.question, name='question'),
    path("user/<str:user_id>/reviews", views.get_user_reviews, name='user_reviews'),
    path("user/<str:user_id>/questions", views.get_user_questions, name='user_questions'),
    path("user/<str:user_id>/answers", views.get_user_answers, name='user_answers'),
    path("notifications", views.notifications, name='notifications'),
    path("notification/read", views.mark_notification_as_read, name='read_notification'),
    path("item", views.item, name='item'),
    path("reviews/<int:item_id>", views.get_reviews_by_item, name='get_reviews_by_item'),
    path("items", views.items, name='items'),
    path("highlighted", views.get_item_with_hl, name='highlighted'),
    path("add/tag", views.add_tag, name='add_tag'),
    path("add/review", views.add_review, name='add_review'),
    path("add/question", views.add_question, name='add_question'),
    path("add/answer", views.add_answer, name='add_answer'),
    path("like/review", views.like_review, name='like_review'),
    path("upvote/question", views.upvote_question, name='upvote_question'),
    path("like/answer", views.like_answer, name='like_answer'),
    path("edit/item", views.edit_item, name='edit_item'),
    path("delete/item", views.delete_item, name='delete_item'),
    path("delete/review", views.delete_review, name='delete_review'),
    path("delete/question", views.delete_question, name='delete_question'),
    path("delete/answer", views.delete_answer, name='delete_answer'),
    path("remove/tag", views.remove_tag, name='remove_tag'),
    path("delete/media", views.delete_media, name='delete_media'),
    path("delete/link", views.delete_link, name='delete_link'),
    path("unlike/review", views.unlike_review, name='unlike_review'),
    path("unlike/answer", views.unlike_answer, name='unlike_answer'),
    path("unupvote/question", views.unupvote_question, name='unupvote_question'),
]