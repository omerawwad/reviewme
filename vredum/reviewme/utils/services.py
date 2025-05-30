from ..models import Review
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