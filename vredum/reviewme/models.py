from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return self.username
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_staff': self.is_staff,
            'is_active': self.is_active,
        }
    

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'added_by': self.added_by.username,
            'reviews': [review.serialize() for review in self.reviews.all()],
            'tags': [tag.name for tag in self.tags.all()],
            'links': [link.url for link in self.links.all()],
            'media': [media.url for media in self.media.all()],
            'questions': [question.serialize() for question in self.questions.all()],
            'review_count': self.reviews.count(),
            'average_rating': self.get_average_rating(),
        }
    
    def brief(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description[:50] + '...',
            'created_at': self.created_at,
            'added_by': self.added_by.username,
        }
    
    def preview(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description[:50] + '...',
            'created_at': self.created_at,
            'added_by': self.added_by.username,
            'media': [media.url for media in self.media.all()[:3]],
            'tags': [tag.name for tag in self.tags.all()],
        }
    
    def get_reviews(self):
        return self.reviews.all()
    
    def get_tags(self):
        return self.tags.all()
    
    def get_links(self):
        return self.links.all()
    
    def get_media(self):
        return self.media.all()    
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.get_rating() for review in reviews)
            return total_rating / len(reviews)
        return 0

class Review(models.Model):
    # rating = models.IntegerField() # making it maximum 5
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # making it maximum 5
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.title
    
    def serialize(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'user': self.user.username,
            'item_id': self.item.id,
        }
    
    def get_rating(self):
        return self.rating

class Link(models.Model):
    url = models.URLField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='links')

    def __str__(self):
        return self.url
    
class Media(models.Model):
    url = models.URLField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='media')

    def __str__(self):
        return self.url
    

class Tag(models.Model):
    name = models.CharField(max_length=50)
    items = models.ManyToManyField(Item, blank=True, related_name='tags')

    def __str__(self):
        return self.name
    
class Question(models.Model):
    text = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text
    
    def serialize(self):
        return {
            'item_id': self.item.id,
            'text': self.text,
            'created_at': self.created_at,
            'created_by': self.created_by.username,
            'answers': [answer.serialize() for answer in self.answers.all()],
        }
    
    
class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.text
    
    def serialize(self):
        return {
            'question': self.question_id,
            'text': self.text,
            'created_at': self.created_at,
            'created_by': self.created_by.username,
            'likes': self.likes.count(),
        }
    

class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_likes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.review.title}"
    
    class Meta:
        unique_together = ('user', 'review')
        verbose_name = 'Review Like'
        verbose_name_plural = 'Review Likes'
    
    def serialize(self):
        return {
            'user': self.user.username,
            'review': self.review.title,
            'created_at': self.created_at,
        }
    
class QuestionUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_upvotes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} upvoted {self.question.text}"
    
    class Meta:
        unique_together = ('user', 'question')
        verbose_name = 'Question Upvote'
        verbose_name_plural = 'Question Upvotes'
    
    def serialize(self):
        return {
            'user': self.user.username,
            'question': self.question.text,
            'created_at': self.created_at,
        }
    
class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.answer.text}"
    
    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = 'Answer Like'
        verbose_name_plural = 'Answer Likes'
    
    def serialize(self):
        return {
            'user': self.user.username,
            'answer': self.answer.text,
            'created_at': self.created_at,
        }
    
