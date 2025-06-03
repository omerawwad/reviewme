from ..models import Review, Item
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