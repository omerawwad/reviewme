from ..models import Review, Item, Question, Answer, ReviewLike, QuestionUpvote, AnswerLike, Notification
from django.core.paginator import Paginator
def get_all_reviews(page=1, page_size=10, sort_by='created_at,desc'):
    """
    Fetch all reviews with pagination and sorted.
    """
    sort_field, order = sort_by.split(',') if sort_by else ('created_at', 'desc')
    try:
        reviwes = Review.objects.all().order_by(f'-{sort_field}' if order == 'desc' else sort_field)
    except Exception as e:
        return {'error': str(e), 'reviews': []}
    if not reviwes:
        return {'error': 'No reviews found', 'reviews': []}
    

    paginator = Paginator(reviwes, page_size)
    try:
        paginated_reviews = paginator.page(page)
    except Exception as e:
        return {'error': str(e), 'reviews': []}
    
    return {
        'reviews': [review.serialize() for review in paginated_reviews],
        'page': page,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'total_reviews': paginator.count
    }

def get_items_by_tag(tag_name, page=1, page_size=10, sort_by='created_at,desc'):
    """
    Fetch all items by tag with pagination and sorted.
    """
    sort_field, order = sort_by.split(',') if sort_by else ('created_at', 'desc')
    try:
        items = Item.objects.filter(tags__name=tag_name).order_by(f'-{sort_field}' if order == 'desc' else sort_field)
    except Exception as e:
        return {'error': str(e), 'items': []}
    if not items:
        return {'error': 'No items found', 'items': []}
    
    paginator = Paginator(items, page_size)
    try:
        paginated_items = paginator.page(page)
    except Exception as e:
        return {'error': str(e), 'items': []}
    
    return {
        'items': [item.serialize() for item in paginated_items],
        'page': page,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'total_items': paginator.count
    }

def search_items(query, page=1, page_size=10, sort_by='created_at,desc'):
    """
    Search for items by name or description with pagination and sorted.
    """
    sort_field, order = sort_by.split(',') if sort_by else ('created_at', 'desc')
    try:
        items = Item.objects.filter(name__icontains=query).order_by(f'-{sort_field}' if order == 'desc' else sort_field)
        if not items:
            return {'error': 'No items found', 'items': []}
        paginator = Paginator(items, page_size)
        try:
            paginated_items = paginator.page(page)
        except Exception as e:
            return {'error': str(e), 'items': []}
        return {
            'items': [item.serialize() for item in paginated_items],
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count
        }
    except Exception as e:
        return {'error': str(e), 'items': []}
    
def get_item(item_id):
    try:
        item = Item.objects.get(id=item_id)
        response = {
            "item": item.serialize(),
            "highlighted": False,
        }
        return response
    except Exception as e:
        return {'error': str(e), 'items': []}
    
def get_item_with_hl_review(review_id):
    try:
        review = Review.objects.get(id=review_id)
        item_id = review.item_id
        item = Item.objects.get(id=item_id)
        response = {
            "item": item.serialize(),
            "highlighted": True,
            "highlighted_type": "review",
            "highlighted_content": review.serialize(),
        }
        return response
    except Exception as e:
        return {'error': str(e), 'items': []}

def get_item_with_hl_question(question_id):
    try:
        question = Question.objects.get(id=question_id)
        item_id = question.item_id
        item = Item.objects.get(id=item_id)
        response = {
            "item": item.serialize(),
            "highlighted": True,
            "highlighted_type": "question",
            "highlighted_content": question.serialize(),
        }
        return response
    except Exception as e:
        return {'error': str(e), 'items': []}
    
def get_user_reviews(user_id, page=1, page_size=10, sort_by='created_at,desc'):
    try:
        reviews = Review.objects.filter(user_id=user_id).order_by(f'-{sort_by.split(",")[0]}' if sort_by.split(",")[1] == 'desc' else sort_by.split(",")[0])
        paginator = Paginator(reviews, page_size)
        try:
            paginated_reviews = paginator.page(page)
        except Exception as e:
            return {'error': str(e), 'reviews': []}

        return {
            'reviews': [review.serialize() for review in paginated_reviews],
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'total_reviews': paginator.count
        }
    except Exception as e:
        return {'error': str(e), 'reviews': []}
    
def get_user_questions(user_id, page=1, page_size=10, sort_by='created_at,desc'):
    try:
        questions = Question.objects.filter(created_by=user_id).order_by(f'-{sort_by.split(",")[0]}' if sort_by.split(",")[1] == 'desc' else sort_by.split(",")[0])
        paginator = Paginator(questions, page_size)
        try:
            paginated_questions = paginator.page(page)
        except Exception as e:
            return {'error': str(e), 'questions': []}
        return {
            'questions': [question.serialize() for question in paginated_questions],
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'total_questions': paginator.count
        }
    except Exception as e:
        return {'error': str(e), 'questions': []}

def get_user_answers(user_id, page=1, page_size=10, sort_by='created_at,desc'):
    try:
        answers = Answer.objects.filter(created_by=user_id).order_by(f'-{sort_by.split(",")[0]}' if sort_by.split(",")[1] == 'desc' else sort_by.split(",")[0])
        paginator = Paginator(answers, page_size)
        try:
            paginated_answers = paginator.page(page)
        except Exception as e:
            return {'error': str(e), 'answers': []}
        return {
            'answers': [answer.serialize_with_question() for answer in paginated_answers],
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'total_answers': paginator.count
        }
    except Exception as e:
        return {'error': str(e), 'answers': []}
    
def get_notifications(user_id):
    try:
        notifications = Notification.objects.filter(user_id=user_id, read=False).order_by('-created_at')
        return {
            'notifications': [notification.serialize() for notification in notifications],
            'total_notifications': notifications.count()
        }
    except Exception as e:
        return {'error': str(e), 'notifications': []}
    
def mark_notification_as_read(user_id, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        if notification.user_id != user_id:
            return {'error': 'You do not have permission to mark this notification as read'}
        notification.mark_as_read()
        return {'success': True, 'message': 'Notification marked as read'}
    except Notification.DoesNotExist:
        return {'error': 'Notification not found'}
    except Exception as e:
        return {'error': str(e)}