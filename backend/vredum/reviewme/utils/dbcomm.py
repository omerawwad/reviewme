from calendar import c
import re
from .authorization import check_same_user
from ..models import Review, Tag, Link, Media, Item, Question, Answer, ReviewLike, QuestionUpvote, AnswerLike

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

def get_user_questions(user_id, page=1, page_size=10):
    # pagination
    start = (page - 1) * page_size
    
    if start < 0 or start >= len(Question.objects.filter(created_by_id=user_id)):
        # print(f"Invalid page number: {page}. Page size: {page_size}.")
        return False, {}
    
    end = len(Question.objects.filter(created_by_id=user_id)) if page * page_size > len(Question.objects.filter(created_by_id=user_id)) else page * page_size

    num_pages = len(Question.objects.filter(created_by_id=user_id)) // page_size + (1 if len(Question.objects.filter(created_by_id=user_id)) % page_size > 0 else 0)

    questions = Question.objects.filter(created_by_id=user_id)[start:end]
    return True, {"questions": [question.serialize() for question in questions], "page": page, "page_size": page_size, "num_pages": num_pages}

def get_user_answers(user_id, page=1, page_size=10):
    # pagination
    start = (page - 1) * page_size
    
    if start < 0 or start >= len(Answer.objects.filter(created_by_id=user_id)):
        # print(f"Invalid page number: {page}. Page size: {page_size}.")
        return False, {}
    
    end = len(Answer.objects.filter(created_by_id=user_id)) if page * page_size > len(Answer.objects.filter(created_by_id=user_id)) else page * page_size

    num_pages = len(Answer.objects.filter(created_by_id=user_id)) // page_size + (1 if len(Answer.objects.filter(created_by_id=user_id)) % page_size > 0 else 0)

    answers = Answer.objects.filter(created_by_id=user_id)[start:end]
    return True, {"answers": [answer.serialize() for answer in answers], "page": page, "page_size": page_size, "num_pages": num_pages}

def like_review(review_id, user_id):
    try:
        review = Review.objects.get(id=review_id)
        print(f"Review: {review}")
    except Review.DoesNotExist:
        print(f"Review with id {review_id} does not exist.")
        return False, {}
    try:
        like = ReviewLike(user_id=user_id, review_id=review_id)
        like.save()
        notification = f"User {user_id} liked review '{review.title}'."
        print(f"User {user_id} liked review '{review.title}'.")
    except Exception as e:
        # print(f"Error liking review: {e}")
        return False, {"errorDuplicateLike": "Like already exists."}
    
    return True, like

def upvote_question(question_id, user_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        print(f"Question with id {question_id} does not exist.")
        return False, {}
    
    try:
        upvote = QuestionUpvote(user_id=user_id, question_id=question_id)
        upvote.save()
        print(f"User {user_id} upvoted question '{question.text}'.")
    except Exception as e:
        # print(f"Error upvoting question: {e}")
        return False, {'errorDuplicateUpvote': "Upvote already exists."}
    
    return True, upvote

def like_answer(answer_id, user_id):
    try:
        answer = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        print(f"Answer with id {answer_id} does not exist.")
        return False, {}
    
    try:
        like = AnswerLike(user_id=user_id, answer_id=answer_id)
        like.save()
        print(f"User {user_id} liked answer '{answer.text}'.")
    except Exception as e:
        # print(f"Error liking answer: {e}")
        return False, {'errorDuplicateLike': "Like already exists."}
    
    return True, like

def edit_item(item_id, user_id, name=None, description=None):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return False, {"errorItemNotFound": "Item not found."}
    
    if not check_same_user(item.added_by_id, user_id):
        print(f"User {user_id} is not authorized to edit this item.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    if name is not None:
        item.name = name
    if description is not None:
        item.description = description
    
    item.save()
    print(f"Item '{item.name}' updated.")
    
    return True, item

def delete_item(item_id, user_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return False, {"errorItemNotFound": "Item not found."}
    
    if not check_same_user(item.added_by_id, user_id):
        print(f"User {user_id} is not authorized to delete this item.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    item.delete()
    print(f"Item '{item.name}' deleted.")
    
    return True, {"message": "Item deleted successfully."}

def delete_review(review_id, user_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        print(f"Review with id {review_id} does not exist.")
        return False, {"errorReviewNotFound": "Review not found."}
    
    if not check_same_user(review.user_id, user_id):
        print(f"User {user_id} is not authorized to delete this review.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    review.delete()
    print(f"Review '{review.title}' deleted.")
    
    return True, {"message": "Review deleted successfully."}

def delete_question(question_id, user_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        print(f"Question with id {question_id} does not exist.")
        return False, {"errorQuestionNotFound": "Question not found."}
    
    if not check_same_user(question.created_by_id, user_id):
        print(f"User {user_id} is not authorized to delete this question.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    question.delete()
    print(f"Question '{question.text}' deleted.")
    
    return True, {"message": "Question deleted successfully."}

def delete_answer(answer_id, user_id):
    try:
        answer = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        print(f"Answer with id {answer_id} does not exist.")
        return False, {"errorAnswerNotFound": "Answer not found."}
    
    if not check_same_user(answer.created_by_id, user_id):
        print(f"User {user_id} is not authorized to delete this answer.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    answer.delete()
    print(f"Answer '{answer.text}' deleted.")
    
    return True, {"message": "Answer deleted successfully."}

def remove_tag(tag_id, item_id, user_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print(f"Item with id {item_id} does not exist.")
        return False, {"errorItemNotFound": "Item not found."}
    
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        print(f"Tag with id {tag_id} does not exist.")
        return False, {"errorTagNotFound": "Tag not found."}
    if not check_same_user(item.added_by_id, user_id):
        print(f"User {user_id} is not authorized to remove this tag.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    item.tags.remove(tag)
    item.save()
    print(f"Tag '{tag.name}' removed from item '{item.name}'.")
    
    return True, {"message": "Tag removed successfully."}

def delete_link(link_id, user_id):
    try:
        link = Link.objects.get(id=link_id)
    except Link.DoesNotExist:
        print(f"Link with id {link_id} does not exist.")
        return False, {"errorLinkNotFound": "Link not found."}
    if not check_same_user(link.item.added_by_id, user_id):
        print(f"User {user_id} is not authorized to delete this link.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    link.delete()
    print(f"Link '{link.url}' deleted.")
    
    return True, {"message": "Link deleted successfully."}

def delete_media(media_id, user_id):
    try:
        media = Media.objects.get(id=media_id)
    except Media.DoesNotExist:
        print(f"Media with id {media_id} does not exist.")
        return False, {"errorMediaNotFound": "Media not found."}
    if not check_same_user(media.item.added_by_id, user_id):
        print(f"User {user_id} is not authorized to delete this media.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    media.delete()
    print(f"Media '{media.url}' deleted.")
    
    return True, {"message": "Media deleted successfully."}

def remove_review_like(review_id, user_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        print(f"Review with id {review_id} does not exist.")
        return False, {"errorReviewNotFound": "Review not found."}
    
    try:
        like = ReviewLike.objects.get(user_id=user_id, review_id=review_id)
    except ReviewLike.DoesNotExist:
        print(f"Like with user id {user_id} and review id {review_id} does not exist.")
        return False, {"errorLikeNotFound": "Like not found."}
    if not check_same_user(like.user_id, user_id):
        print(f"User {user_id} is not authorized to remove this like.")
        return False, {"errorUnauthorized": "User not authorized."}
    like.delete()
    print(f"Like removed from review '{review.title}' by user '{user_id}'.")
    
    return True, {"message": "Like removed successfully."}

def remove_question_upvote(question_id, user_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        print(f"Question with id {question_id} does not exist.")
        return False, {"errorQuestionNotFound": "Question not found."}
    
    try:
        upvote = QuestionUpvote.objects.get(user_id=user_id, question_id=question_id)
    except QuestionUpvote.DoesNotExist:
        print(f"Upvote with user id {user_id} and question id {question_id} does not exist.")
        return False, {"errorUpvoteNotFound": "Upvote not found."}
    
    if not check_same_user(upvote.user_id, user_id):
        print(f"User {user_id} is not authorized to remove this upvote.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    upvote.delete()
    print(f"Upvote removed from question '{question.text}' by user '{user_id}'.")
    
    return True, {"message": "Upvote removed successfully."}

def remove_answer_like(answer_id, user_id):
    try:
        answer = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        print(f"Answer with id {answer_id} does not exist.")
        return False, {"errorAnswerNotFound": "Answer not found."}
    
    try:
        like = AnswerLike.objects.get(user_id=user_id, answer_id=answer_id)
    except AnswerLike.DoesNotExist:
        print(f"Like with user id {user_id} and answer id {answer_id} does not exist.")
        return False, {"errorLikeNotFound": "Like not found."}
    
    if not check_same_user(like.user_id, user_id):
        print(f"User {user_id} is not authorized to remove this like.")
        return False, {"errorUnauthorized": "User not authorized."}
    
    like.delete()
    print(f"Like removed from answer '{answer.text}' by user '{user_id}'.")
    
    return True, {"message": "Like removed successfully."}