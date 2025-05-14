from calendar import c
from .authorization import check_same_user
from ..models import Review, Tag, Link, Media, Item, Question, Answer

def get_item_by_id(item_id):
    try:
        item = Item.objects.get(id=item_id)
        return item
    except Item.DoesNotExist:
        # print(f"Item with id {item_id} does not exist.")
        return None

def get_tag_by_id(tag_id):
    try:
        tag = Tag.objects.get(id=tag_id)
        return tag
    except Tag.DoesNotExist:
        print(f"Tag with id {tag_id} does not exist.")
        return None
def get_Tag(tag_name):
    try:
        tag = Tag.objects.get(name=tag_name)
        return tag
    except Tag.DoesNotExist:
        return None
    
def create_Tag(tag_name):
    tag = get_Tag(tag_name)
    if tag is None:
        tag = Tag(name=tag_name)
        tag.save()
        print(f"Tag '{tag_name}' created.")
    return tag

def get_tags():
    tags = Tag.objects.all()
    return [tag.name for tag in tags]

def get_item_tags(item_id):
    item = Item.objects.get(id=item_id)
    return [tag.name for tag in item.tags.all()]

def create_link(item_id, url):
    try:
        link = Link(url=url, item_id=item_id)
        link.save()
        return link
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return None
    
def create_media(item_id, url):
    try:
        media = Media(url=url, item_id=item_id)
        media.save()
        return media
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return None
    


        

def add_tags_to_item(item, tags):
    warnings = []
    for tag in tags:
        current_tag = create_Tag(tag)
        try:
            # Check if the tag already exists
            if current_tag in item.tags.all():
                warnings.append(f"Tag '{tag}' already exists in item '{item.name}'.")
            else:
                item.tags.add(current_tag)
                item.save()
        except Exception as e:
            print(f"Error adding tag '{tag}' to item: {e}")
            return False
    return True, warnings


def add_links_to_item(item_id, urls):
    for url in urls:
        create_link(item_id, url)
    return True

def add_media_to_item(item_id, urls):
    for url in urls:
        create_media(item_id, url)
    return True

def get_items(page=1, page_size=10):
    
    # pagination
    start = (page - 1) * page_size
    
    if start < 0 or start >= len(Item.objects.all()):
        # print(f"Invalid page number: {page}. Page size: {page_size}.")
        return False,{}
    
    end = len(Item.objects.all()) if page * page_size > len(Item.objects.all()) else page * page_size

    num_pages = len(Item.objects.all()) // page_size + (1 if len(Item.objects.all()) % page_size > 0 else 0)

    items = Item.objects.all()[start:end]
    return True,{"items": [item.serialize() for item in items], "page": page, "page_size": page_size, "num_pages": num_pages}

def get_item(item_id):
    try:
        item = Item.objects.get(id=item_id)
        response = {
            "item": item.serialize(),
            "highlighted": False,
        }
        return True, response
    except Item.DoesNotExist:
        # print(f"Item with id {item_id} does not exist.")
        return False, {}

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
        return True, response
    except Item.DoesNotExist:
        # print(f"Item with id {item_id} does not exist.")
        return False, {}
    except review.DoesNotExist:
        # print(f"Review with id {review_id} does not exist.")
        response = {
            "item": item.serialize(),
            "highlighted": False,
        }
        return True, response
    
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
        return True, response
    except Item.DoesNotExist:
        # print(f"Item with id {item_id} does not exist.")
        return False, {}
    except Question.DoesNotExist:
        # print(f"Question with id {question_id} does not exist.")
        response = {
            "item": item.serialize(),
            "highlighted": False,
        }
        return True, response


def get_item_by_name(item_name):
    try:
        item = Item.objects.get(name=item_name)
        return item.serialize()
    except Item.DoesNotExist:
        print(f"Item with name {item_name} does not exist.")
        return None


def create_item(name, user_id, description=None, tags=None, links=None, media=None):
    if get_item_by_name(name) is not None:
        print(f"Item with name '{name}' already exists.")
        return None
    
    item = Item(name=name, added_by_id=user_id, description=description)
    item.save()
    print(f"Item '{name}' created.")
    
    # Add links to item
    if links is not None:
        add_links_to_item(item.id, links)
        # add_item_links(item.id, links)
        print(f"Links: {links}")
    # Add media to item
    if media is not None:
        add_media_to_item(item.id, media)
        # add_item_media(item.id, media)
        print(f"Media: {media}")
    # Add tags to item
    add_tags_to_item(item, tags)
    # add_item_tags(item, tags)
    print(f"Tags: {tags}")

    # created_item = get_item(item.id)

    return item

def update_item(item_id, user_id, name=None, description=None, tags=None, links=None, media=None):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return None
    
    if not check_same_user(item.added_by_id, user_id):
        print(f"User {item.added_by_id} is not authorized to update this item.")
        return None

    
    if name is not None:
        item.name = name
    if description is not None:
        item.description = description
    if tags is not None:
        add_tags_to_item(item, tags)
    if links is not None:
        add_links_to_item(item.id, links)
    if media is not None:
        add_media_to_item(item.id, media)
    
    item.save()
    print(f"Item '{item.name}' updated.")
    
    return item

# def delete_item(item_id, user_id):

def add_tags(item_id, tags):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return False
    return add_tags_to_item(item, tags)

def remove_tags(item_id, tags):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return False
    for tag in tags:
        try:
            item.tags.remove(tag)
        except Exception as e:
            print(f"Error removing tag '{tag}' from item: {e}")
            return False
    return True


def create_review(item_id, user_id, rating, title, description):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return False, {}
    
    review = Review(item=item, user_id=user_id, rating=rating, title=title, description=description)
    review.save()
    print(f"Review '{title}' created.")
    
    return True, review

def create_question(item_id, user_id, text):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return False, {}
    
    question = Question(item=item, created_by_id=user_id, text=text)
    question.save()
    print(f"Question '{text}' created.")
    
    return True, question

def create_answer(question_id, user_id, text):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        print(f"Question with id {question_id} does not exist.")
        return False, {}
    
    answer = Answer(question=question, created_by_id=user_id, text=text)
    answer.save()
    print(f"Answer '{text}' created.")
    
    return True, answer

def get_user_reviews(user_id, page=1, page_size=10):
    # pagination
    start = (page - 1) * page_size
    
    if start < 0 or start >= len(Review.objects.filter(user_id=user_id)):
        # print(f"Invalid page number: {page}. Page size: {page_size}.")
        return False, {}
    
    end = len(Review.objects.filter(user_id=user_id)) if page * page_size > len(Review.objects.filter(user_id=user_id)) else page * page_size

    num_pages = len(Review.objects.filter(user_id=user_id)) // page_size + (1 if len(Review.objects.filter(user_id=user_id)) % page_size > 0 else 0)

    reviews = Review.objects.filter(user_id=user_id)[start:end]
    return True, {"reviews": [review.serialize() for review in reviews], "page": page, "page_size": page_size, "num_pages": num_pages}