from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validateRegistration(self, form):
        errors = []

        if len(form['first_name']) == 0:
            errors.append("First Name is required")
        elif len(form['first_name'])<2:
            errors.append("First Name must be longer than 2 characters")
        if len(form['last_name']) == 0:
            errors.append("Last Name is required")
        elif len(form['last_name'])<2:
            errors.append("Last Name must be longer than 2 characters!")
        if len(form['email']) == 0:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(form['email']):
            errors.append("Please enter a valid Email")
        elif Users.objects.filter(email=form['email']):
            errors.append("Account already exists with that Email")

        if len(form['password']) == 0:
            errors.append("Password is required")
        elif len(form['password'])<8:
            errors.append("Password must be at least 8 characters")
        if form['passconf'] != form['password']:
            errors.append("Passwords Don't Match")

        return errors

    def register(self, form):
        hashed_pass = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        return self.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=hashed_pass)

    def check_login(self, form):
        check_user = self.filter(email=form['email'])
        if check_user:
            user = check_user[0]
            if bcrypt.hashpw(form['password'].encode(), user.password.encode()) == user.password:
                return user
        else:
            return None


# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
