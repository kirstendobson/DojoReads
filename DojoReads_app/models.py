from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def validator(self, postData):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postData['name']) < 3:
            errors['name'] = "Name must be at least 3 characters"
        if len(postData['username']) < 3:
            errors['username'] = "Username must be at least 3 characters"
        if not email_check.match(postData['email']):
            errors['email'] = "Email must be a valid email address"
        if postData['pword'] != postData['cnfrm_pword']:
            errors['pword_match'] = "Password and Confirm Password must match"
        if len(postData['pword']) < 8:
            errors['pword'] = "Password must be at least 8 characters"
        check = User.objects.filter(email=postData['email'])
        if check:
            errors['emails'] = "Email is already in use"
        return errors
    def login_validator(self, postData):
        errors={}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered"
        else:
            if not bcrypt.checkpw(postData['login_pword'].encode(), check[0].pword.encode()):
                errors['login_email'] = "Email and password do not match"
        return errors
    def edit_validator(self, postData):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if not email_check.match(postData['email']):
            errors['email'] = "Email must be a valid email address"
        check = User.objects.filter(email=postData['email'])
        if check:
            errors['emails'] = "Email is already registered"
        if len(postData['name']) < 1:
            errors['name'] = "Name cannot be blank"
        if len(postData['l_name']) < 1:
            errors['username'] = "Username cannot be blank"
        if len(postData['email']) < 1:
            errors['email'] = "Email cannot be blank"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class AuthorManager(models.Manager):
    def author_validator(self, postData):
        errors={}
        if len(postData['author_name']) < 2:
            errors['author_name'] = "Author name should be at least 2 characters"
        return errors

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors={}
        check = Book.objects.filter(title=postData['title'])
        if check:
            errors['titles'] = "A book with that title already exists"
        if len(postData['title']) < 3:
            errors['title'] = "Title must be at least 3 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors={}
        if len(postData['review']) < 10:
            errors['review'] = "Review should be at least 10 characters long"
        if int(postData['rating']) < 1 or int(postData['rating']) > 5:
            errors['rating'] = "Rating should be 1 to 5 stars"
        return errors

class Review(models.Model):
    content = models.CharField(max_length=255)
    rating = models.IntegerField()
    book = models.ForeignKey(Book, related_name="reviews", on_delete = models.CASCADE)
    posted_by = models.ForeignKey(User, related_name="reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()