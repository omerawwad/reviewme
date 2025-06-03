from calendar import c
from email import message
import json
from os import name
import re
from urllib import response
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from numpy import empty
from pygments import highlight




from .utils import dbcomm
from .utils import conversion
from .utils import auth
from .utils import services
from .utils import request_parser


# Create your views here.
def index(request):
    # dbcomm.create_item(name='Test Item', description='This is a test item.', user_id=1, media=['https://image_example.com', 'https://image_example2.com'], links=['https://example.com', 'https://example2.com'],tags=['tag1', 'tag2'])
    # print(dbcomm.get_items())
    user = request.user
    authnticate = auth.get_user_id(request)
    print(authnticate)
    return render(request, 'reviewme/index.html')

# Public APIs ( items -> Fetch All Items,  item/<item_id> -> Fetch Item by ID )

def reviews(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'UNAUTHORIZED'}, status=401)
    
    page, size = request_parser.get_page_details(request.GET)
    response = services.get_all_reviews(page=page, page_size=size)

    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

def get_items_by_tag(request, tag_name):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    page, size = request_parser.get_page_details(request.GET)
    response = services.get_items_by_tag(tag_name=tag_name, page=page, page_size=size)

    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

def search_items(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    if not request.GET.get('search'):
        return JsonResponse({'error': 'Search query is required'}, status=404)

    search_query = request.GET.get('search')
    page, size = request_parser.get_page_details(request.GET)
    response = services.search_items(search_query=search_query, page=page, page_size=size)

    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

def search_items(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    if not request.GET.get('query'):
        return JsonResponse({'error': 'Query parameter is required'}, status=404)
    query = request.GET.get('query', '').strip()
    page, size = request_parser.get_page_details(request.GET)

    response = services.search_items(query=query, page=page, page_size=size)
    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

def get_item(request, item_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    response = services.get_item(item_id=item_id)

    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

def review(request, review_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    response = services.get_item_with_hl_review(review_id=review_id)
    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

def question(request, question_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    response = services.get_item_with_hl_question(question_id=question_id)
    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)
    
def get_user_reviews(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    page, size = request_parser.get_page_details(request.GET)
    response = services.get_user_reviews(user_id=user_id, page=page, page_size=size)
    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

def get_user_questions(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    page, size = request_parser.get_page_details(request.GET)
    response = services.get_user_questions(user_id=user_id, page=page, page_size=size)
    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

def get_user_answers(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    page, size = request_parser.get_page_details(request.GET)
    response = services.get_user_answers(user_id=user_id, page=page, page_size=size)
    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

@login_required
def notifications(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    user_id = auth.get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    response = services.get_notifications(user_id=user_id)
    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

# @csrf_exempt
@login_required
def mark_notification_as_read(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    user_id = auth.get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'User not authenticated'}, status=404)
    data = json.loads(request.body)
    notification_id = request_parser.get_notification_id(data)
    if notification_id is None:
        return JsonResponse({'error': 'Notification ID is required'}, status=400)
    
    response = services.mark_notification_as_read( user_id=user_id, notification_id=notification_id)
    if 'error' in response:
        return JsonResponse({'error': response['error']}, status=404)
    return JsonResponse(response, safe=False)

def items(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    # parameters must be integers
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
    except ValueError:
        return JsonResponse({'error': 'Invalid page or page_size parameter'}, status=400)
   
    # parameters must be positive integers
    if page < 1 or page_size < 1:
        return JsonResponse({'error': 'Page and page_size must be positive integers'}, status=400)

    response, result = dbcomm.get_items(page=page, page_size=page_size)
    
    if not response:
        return JsonResponse({'error': 'Page Does Not Exist'}, status=400)

    return JsonResponse(result, safe=False)



def get_item_with_hl(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    highlighted_review = request.GET.get('highlighted_review', None)
    highlighted_question = request.GET.get('highlighted_question', None)
    
    if highlighted_review:
        try:
            review_id = int(highlighted_review)
        except ValueError:
            return JsonResponse({'error': 'Invalid review ID'}, status=400)
        
        response, result = dbcomm.get_item_with_hl_review(review_id=review_id)
        
        if not response:
            return JsonResponse({'error': 'Review Does Not Exist'}, status=400)
        return JsonResponse(result, safe=False)
    
   
    if highlighted_question:
        try:
            question_id = int(highlighted_question)
        except ValueError:
            return JsonResponse({'error': 'Invalid question ID'}, status=400)

        response, result = dbcomm.get_item_with_hl_question(question_id=question_id)
        
        if not response:
            return JsonResponse({'error': 'Question Does Not Exist'}, status=400)
        return JsonResponse(result, safe=False)


# Private APIs ( create_item -> Create Item, update_item -> Update Item, delete_item -> Delete Item )

@login_required
def item(request):
    # if request.method == 'GET':
    #     return JsonResponse({'error': 'Invalid request'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    user = request.user    
    user_id = user.id
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    name = data.get('name')
    description = data.get('description')
    tags = data.getlist('tags')
    links = data.getlist('links')
    media = data.getlist('media')
    
    if request.method == 'POST':

        # Validate the input
        if not name or not user_id:
            return JsonResponse({'error': 'Name and user_id are required'}, status=400)

        # Create the item
        item = dbcomm.create_item(name=name, user_id=user_id, description=description, tags=tags, links=links, media=media)
        
        if not item:
            return JsonResponse({'error': 'Item already exists'}, status=400)

        return JsonResponse(item.serialize(), safe=False)
    
    elif request.method == 'PUT':
        item_id = data.get('item_id')
        # Validate the input
        if not item_id or not user_id:
            return JsonResponse({'error': 'Item id and user are required'}, status=400)

        # Update the item
        item = dbcomm.update_item(item_id=int(item_id), user_id=user_id, name=name, description=description, tags=tags, links=links, media=media)
        
        if not item:
            return JsonResponse({'error': 'Item does not exist'}, status=400)

        return JsonResponse(item.serialize(), safe=False)
    

@login_required
def add_tag(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    warning = []
    user = request.user
    user_id = user.id
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    tags = data.getlist('tags')
    item_id = data.get('item_id')
    
    # Validate the input
    if not item_id or not user_id:
        return JsonResponse({'error': 'Item id and user are required'}, status=400)
    if not tags:
        return JsonResponse({'error': 'Tags are required'}, status=400)
    
    if conversion.check_item_id(item_id) == False:
        return JsonResponse({'error': 'Item does not exist'}, status=400)
    
    # converted_tags_ids = conversion.convert_ids_to_int(tags_ids)
    valid_tags, warnings_from_checking_tags = conversion.check_tags(tags)
    if not valid_tags:
        return JsonResponse({'error': 'Invalid tags'}, status=400)
    if len(warnings_from_checking_tags) > 0:
        warning.extend(warnings_from_checking_tags)

    # Add the tags to the item
    response, warning_from_adding_tags = dbcomm.add_tags(item_id=int(item_id), tags=valid_tags)
    
    if len(warning_from_adding_tags) > 0:
        warning.extend(warning_from_adding_tags)

    if not response:
        return JsonResponse({'error': 'Item does not exist'}, status=400)
    return JsonResponse({'message': 'Request done successfully', 'warning': warning}, status=200)

@login_required
def add_review(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    rating = 0

    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    item_id = data.get('item_id')
    title = data.get('review_title')
    description = data.get('review_description')

    if data.get('rating'):
        # Check if the rating is between 1 and 5
        try:
            review_rating = int(data.get('rating'))
        except ValueError:
            return JsonResponse({'error': 'Rating must be an integer'}, status=400)
        
        # Check if the rating is between 1 and 5
        if review_rating > 0 and review_rating < 6:
            rating = review_rating

    # if data.get('rating') and data.get('rating') > 0 and data.get('rating') < 6:
    #     rating = data.get('rating')

    # if int(review_rating) > 5 or int(review_rating) < 1:
    #     return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
    
    # Validate the input
    if not item_id or not user_id:
        return JsonResponse({'error': 'Item id and user are required'}, status=400)
    
    if conversion.check_item_id(item_id) == False:
        return JsonResponse({'error': 'Item does not exist'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.create_review(item_id=int(item_id), user_id=user_id, rating=rating, title=title, description=description)
    
    if not response:
        return JsonResponse({'error': 'Item does not exist'}, status=400)

    return JsonResponse(result.serialize(), safe=False)
    

@login_required
def add_question(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    item_id = data.get('item_id')
    text = data.get('question_text')
    # Validate the input
    if not item_id or not user_id:
        return JsonResponse({'error': 'Item id and user are required'}, status=400)
    
    if conversion.check_item_id(item_id) == False:
        return JsonResponse({'error': 'Item does not exist'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.create_question(item_id=int(item_id), user_id=user_id, text=text)
    
    if not response:
        return JsonResponse({'error': 'Item does not exist'}, status=400)

    return JsonResponse(result.serialize(), safe=False)


@login_required
def add_answer(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    question_id = data.get('question_id')
    text = data.get('answer_text')
    # Validate the input
    if not question_id or not user_id:
        return JsonResponse({'error': 'Question id and user are required'}, status=400)
    
    if conversion.check_item_id(question_id) == False:
        return JsonResponse({'error': 'Question does not exist'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.create_answer(question_id=int(question_id), user_id=user_id, text=text)
    
    if not response:
        return JsonResponse({'error': 'Question does not exist'}, status=400)

    return JsonResponse(result.serialize(), safe=False)

@login_required
def like_review(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    review_id = data.get('review_id')

    if not review_id:
        return JsonResponse({'error': 'Review id is required'}, status=400)

    try:
        review_id = int(review_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid review ID'}, status=400)

    # Validate the input
    if not review_id or not user_id:
        return JsonResponse({'error': 'Review id and user are required'}, status=400)
    
    print(f"Review ID: {review_id}")
    # Add the review to the item
    response, result = dbcomm.like_review(review_id=int(review_id), user_id=user_id)
    print(result)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result.serialize(), safe=False)

@login_required
def upvote_question(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user = request.user
    user_id = user.id
    question_id = data.get('question_id')
    # print(f"Question ID: {question_id}

    if not question_id:
        return JsonResponse({'error': 'Question id is required'}, status=400)
    try:
        question_id = int(question_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid question ID'}, status=400)

    # Validate the input
    if not question_id or not user_id:
        return JsonResponse({'error': 'Question id and user are required'}, status=400)
    
    print(f"Question ID: {question_id}")
    # Add the review to the item
    response, result = dbcomm.upvote_question(question_id=question_id, user_id=user_id)
    print(result)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result.serialize(), safe=False)

@login_required
def like_answer(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    answer_id = data.get('answer_id')

    if not answer_id:
        return JsonResponse({'error': 'Answer id is required'}, status=400)

    try:
        answer_id = int(answer_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid answer ID'}, status=400)

    # Validate the input
    if not answer_id or not user_id:
        return JsonResponse({'error': 'Answer id and user are required'}, status=400)
    
    print(f"Answer ID: {answer_id}")
    # Add the review to the item
    response, result = dbcomm.like_answer(answer_id=answer_id, user_id=user_id)
    # print(result)
    if not response:
        return JsonResponse(result, status=400)
    return JsonResponse(result.serialize(), safe=False)

@login_required
def edit_item(request):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    item_id = data.get('item_id')
    name = data.get('name')
    description = data.get('description')


    
    # Validate the input
    if not item_id or not user_id:
        return JsonResponse({'error': 'Item id and user are required'}, status=400)
    
    try:
        item_id = int(item_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid item ID'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.edit_item(item_id=item_id, user_id=user_id, name=name, description=description)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result.serialize(), safe=False)


@login_required
def delete_item(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    item_id = data.get('item_id')
    
    # Validate the input
    if not item_id or not user_id:
        return JsonResponse({'error': 'Item id and user are required'}, status=400)
    
    try:
        item_id = int(item_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid item ID'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.delete_item(item_id=item_id, user_id=user_id)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse({"message":"Item deleted successfully"}, safe=False)

@login_required
def delete_review(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    review_id = data.get('review_id')
    
    # Validate the input
    if not review_id or not user_id:
        return JsonResponse({'error': 'Review id and user are required'}, status=400)
    
    try:
        review_id = int(review_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid review ID'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.delete_review(review_id=review_id, user_id=user_id)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result, safe=False)

@login_required
def delete_question(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    question_id = data.get('question_id')
    
    # Validate the input
    if not question_id or not user_id:
        return JsonResponse({'error': 'Question id and user are required'}, status=400)
    
    try:
        question_id = int(question_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid question ID'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.delete_question(question_id=question_id, user_id=user_id)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result, safe=False)

@login_required
def delete_answer(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    answer_id = data.get('answer_id')
    
    # Validate the input
    if not answer_id or not user_id:
        return JsonResponse({'error': 'Answer id and user are required'}, status=400)
    
    try:
        answer_id = int(answer_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid answer ID'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.delete_answer(answer_id=answer_id, user_id=user_id)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result, safe=False)


@login_required
def remove_tag(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    item_id = data.get('item_id')
    tag_id = data.get('tag_id')
    
    # Validate the input
    if not item_id or not user_id:
        return JsonResponse({'error': 'Item id and user are required'}, status=400)
    
    try:
        item_id = int(item_id)
        tag_id = int(tag_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid item ID or tag ID'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.remove_tag(item_id=item_id, user_id=user_id, tag_id=tag_id)
    if not response:
        return JsonResponse(result, status=400)
    return JsonResponse(result, safe=False)

@login_required
def delete_media(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    media_id = data.get('media_id')
    
    # Validate the input
    if not media_id or not user_id:
        return JsonResponse({'error': 'Media id and user are required'}, status=400)
    
    try:
        media_id = int(media_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid media ID'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.delete_media(media_id=media_id, user_id=user_id)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result, safe=False)

@login_required
def delete_link(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    link_id = data.get('link_id')
    
    # Validate the input
    if not link_id or not user_id:
        return JsonResponse({'error': 'Link id and user are required'}, status=400)
    
    try:
        link_id = int(link_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid link ID'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.delete_link(link_id=link_id, user_id=user_id)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result, safe=False)


@login_required
def unlike_review(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    review_id = data.get('review_id')

    if not review_id:
        return JsonResponse({'error': 'Review id is required'}, status=400)

    try:
        review_id = int(review_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid review ID'}, status=400)

    # Validate the input
    if not review_id or not user_id:
        return JsonResponse({'error': 'Review id and user are required'}, status=400)
    
    print(f"Review ID: {review_id}")
    # Add the review to the item
    response, result = dbcomm.remove_review_like(review_id=int(review_id), user_id=user_id)
    print(result)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result, safe=False)

@login_required
def unupvote_question(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    question_id = data.get('question_id')

    if not question_id:
        return JsonResponse({'error': 'Question id is required'}, status=400)

    try:
        question_id = int(question_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid question ID'}, status=400)

    # Validate the input
    if not question_id or not user_id:
        return JsonResponse({'error': 'Question id and user are required'}, status=400)
    
    print(f"Question ID: {question_id}")
    # Add the review to the item
    response, result = dbcomm.remove_question_upvote(question_id=int(question_id), user_id=user_id)
    print(result)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result, safe=False)

@login_required
def unlike_answer(request):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
     # Get the data from the request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    user = request.user
    user_id = user.id
    answer_id = data.get('answer_id')

    if not answer_id:
        return JsonResponse({'error': 'Answer id is required'}, status=400)

    try:
        answer_id = int(answer_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid answer ID'}, status=400)

    # Validate the input
    if not answer_id or not user_id:
        return JsonResponse({'error': 'Answer id and user are required'}, status=400)
    
    print(f"Answer ID: {answer_id}")
    # Add the review to the item
    response, result = dbcomm.remove_answer_like(answer_id=int(answer_id), user_id=user_id)
    print(result)
    
    if not response:
        return JsonResponse(result, status=400)

    return JsonResponse(result, safe=False)

def tag_items(request, tag_name):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    page, size = requet_parser.get_page_details(request.GET)
    tag = dbcomm.get_Tag(tag_name)
    if not tag:
        return JsonResponse({'error': 'Tag not found'}, status=404)
    items = tag.items.all()
    total = items.count()
    start = (page - 1) * size
    end = start + size
    paginated = items[start:end]
    result = {
        'items': [item.brief() for item in paginated],
        'page': page,
        'page_size': size,
        'total_items': total,
        'total_pages': (total + size - 1) // size
    }
    return JsonResponse(result, safe=False)





def user_reviews(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    page, size = requet_parser.get_page_details(request.GET)
    response = dbcomm.get_user_reviews(user_id=user_id, page=page, page_size=size)
    if not response[0]:
        return JsonResponse({'error': 'User or reviews not found'}, status=404)
    return JsonResponse(response[1], safe=False)


def user_questions(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    page, size = requet_parser.get_page_details(request.GET)
    response = dbcomm.get_user_questions(user_id=user_id, page=page, page_size=size)
    if not response[0]:
        return JsonResponse({'error': 'User or questions not found'}, status=404)
    return JsonResponse(response[1], safe=False)


def user_answers(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    page, size = requet_parser.get_page_details(request.GET)
    response = dbcomm.get_user_answers(user_id=user_id, page=page, page_size=size)
    if not response[0]:
        return JsonResponse({'error': 'User or answers not found'}, status=404)
    return JsonResponse(response[1], safe=False)



