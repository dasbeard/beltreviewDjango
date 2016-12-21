from __future__ import unicode_literals

from django.db import models
from ..loginReg.models import Users

# class ReviewManager(models.Manager):
#     def create_review(self, form, user_id):
#         book = self.fetch_book(form)
#         user = User.objects.get(id=user_id)
#         new_review = Review.objects.create(content=form['review'], rating=form['rating'], user=user, book = book)
#         return (True, new_review)
#
#     def fetch_book(self, form):
#         book = Book.objects.get(id=form['book_id'])
#         author = self.fetch_author(form)
#         book = Book.objects.create(title=form['title'], author = author)
#         return book
#
#     def fetch_author(self, form):
#         author = Author.objects.get(id=form['author_id'])
#
#     def fetch_recent(self):
#         return Review.objects.all().order_by('-created_at')[:3]

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', related_name="theAuthor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey('loginReg.Users', related_name="theUser")
    book = models.ForeignKey('Book', related_name="theBook")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # objects = ReviewManager()
