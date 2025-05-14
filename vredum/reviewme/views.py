from calendar import c
import json
from urllib import response
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from numpy import empty
from pygments import highlight



from .utils import dbcomm
from .utils import conversion


# Create your views here.
def index(request):
    # dbcomm.create_item(name='Test Item', description='This is a test item.', user_id=1, media=['https://image_example.com', 'https://image_example2.com'], links=['https://example.com', 'https://example2.com'],tags=['tag1', 'tag2'])
    # print(dbcomm.get_items())
    return render(request, 'reviewme/index.html')

# Public APIs ( items -> Fetch All Items,  item/<item_id> -> Fetch Item by ID )

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

def get_item(request, item_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    response, result = dbcomm.get_item(item_id=item_id)
    
    if not response:
        return JsonResponse({'error': 'Item Does Not Exist'}, status=400)

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

def review(request, review_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    response, result = dbcomm.get_item_with_hl_review(review_id=review_id)

    if not response:
        return JsonResponse({'error': 'Review Does Not Exist'}, status=400)

    return JsonResponse(result, safe=False)

def question(request, question_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
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
    data = request.POST
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
    data = request.POST
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
    data = request.POST
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
    data = request.POST
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
    data = request.POST
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
def get_user_reviews(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    user = request.user
    user_id = user.id
    
    # Get the data from the request
    data = request.POST
    item_id = data.get('item_id')
    
    # Validate the input
    if not user_id:
        return JsonResponse({'error': 'Item id and user are required'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.get_user_reviews(user_id=user_id)
    
    if not response:
        return JsonResponse({'error': 'Item does not exist'}, status=400)

    return JsonResponse({"result": result, "user": user.username}, safe=False)

def get_user_questions(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    user = request.user
    user_id = user.id
    
    # Get the data from the request
    data = request.POST
    item_id = data.get('item_id')
    
    # Validate the input
    if not user_id:
        return JsonResponse({'error': 'Item id and user are required'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.get_user_questions(user_id=user_id)
    
    if not response:
        return JsonResponse({'error': 'Item does not exist'}, status=400)

    return JsonResponse({"result": result, "user": user.username}, safe=False)

def get_user_answers(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    user = request.user
    user_id = user.id
    
    # Get the data from the request
    data = request.POST
    item_id = data.get('item_id')
    
    # Validate the input
    if not user_id:
        return JsonResponse({'error': 'Item id and user are required'}, status=400)
    
    # Add the review to the item
    response, result = dbcomm.get_user_answers(user_id=user_id)
    
    if not response:
        return JsonResponse({'error': 'Item does not exist'}, status=400)

    return JsonResponse({"result": result, "user": user.username}, safe=False)

@login_required
def like_review(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    # Get the data from the request
    data = request.POST
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
    data = request.POST
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
    data = request.POST
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


    