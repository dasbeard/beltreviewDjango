from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..loginReg.models import Users
from . import models
from models import Book, Author, Review


# Create your views here.
def index(request):
    if not 'logged_user'in request.session:
        return redirect(reverse('users:index'))
    else:
        user = Users.objects.filter(pk=request.session['logged_user'])
    context = {
        'reviews' : Review.objects.all().order_by('-created_at')[:3],
        'all_reviews' : Review.objects.order_by('created_at'),
        'user': user[0],
        }

    return render(request, 'books/index.html', context)

def add(request):
    #Add Book Page
    if not 'logged_user'in request.session:
        return redirect(reverse('users:index'))
    oldAuthors = models.Author.objects.all()
    context = {'oldAuthors':oldAuthors}
    return render(request, 'books/add.html', context)

def create_book(request):
    #Create a Book, Author and add review
    if not 'logged_user'in request.session:
        return redirect(reverse('users:index'))
    else:
        user = Users.objects.get(pk=request.session['logged_user'])
    errors=[]
    form = request.POST

    book_title = form['title']
    if len(book_title)<1:
        errors.append("Book Title can not be blank")

    if len(form['newAuthor']) <1:
        author = form['author']
    else:
        author = form['newAuthor']
    # author = form['newAuthor']
    # if len(author)<1:
    #     errors.append("Author Name can not be blank")

    review = form['review']
    if len(review)<1:
        errors.append("Review can not be blank")

    rating = form['rating']

    if errors:
        for error in errors:
            messages.error(request, error)
            return redirect(reverse('books:add'))

    add_author = models.Author(name=author)
    add_author.save()

    add_book = models.Book(title=book_title, author=add_author)
    add_book.save()

    add_review = models.Review(content=review, rating=rating, user=user, book=add_book)
    add_review.save()

    return redirect(reverse('books:index'))


def create_review (request, id):
    user = Users.objects.filter(pk=request.session['logged_user'])
    if request.POST:

        rating = request.POST['rating']
        review = request.POST['review']
        if len(review)<1:
            messages.error(request, "Review can not be blank")
            return redirect ('books:book', id=id)
        else:
            reviewed = models.Review.objects.filter(book__id=id, user__id=user)
            if reviewed:
                messages.error(request, "You can't review a book twice")
                return redirect ('books:book', id=id)
            book = models.Book.objects.get(pk=id)

            add_review = models.Review(content=review, rating=rating, user=user[0], book=book)
            add_review.save()

        return redirect ('books:book', id=id)

def book(request, id):
    if not 'logged_user'in request.session:
        return redirect(reverse('users:index'))
    else:
        user = Users.objects.get(pk=request.session['logged_user'])

    allReviews = Review.objects.filter(book__id=id)
    book = Book.objects.get(id=id)

    context = {
    'book': book,
    'allReviews':allReviews,
    'logged_user':user,
    }
    return render(request, 'books/review.html', context)

def user(request, id):
    if not 'logged_user'in request.session:
        return redirect(reverse('users:index'))
    books = models.Review.objects.filter(user__id=id)
    user = models.Users.objects.get(id=id)
    count = models.Review.objects.filter(user__id=id).count()

    context ={
        'books':books,
        'user': user,
        'count': count,
    }
    return render(request, 'books/user.html', context)

def delete(request, id):
    review = models.Review.objects.get(id=id)
    context = {
        'review':review,
    }
    book = review.book.id
    review.delete()
        # print "deleted"
    return redirect('/books/'+str(book))
