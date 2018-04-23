from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def nameValidator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name must be at least 3 characters long"
        elif not re.match('[A-Za-z]+', postData['first_name']):
            errors['last_name'] = "Why do you have numbers in your name dude."
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name must be at least 3 characters long"
        elif not re.match('[A-Za-z]+', postData['last_name']):
            errors['last_name'] = "Why do you have numbers in your last name dude"
        if len(postData['email']) < 1:
            errors['email'] = "Please enter an email"
        elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', postData['email']):
            errors['email'] = "Bro, check your email"
        elif User.objects.filter(email=postData['email']):
            errors['email'] = "Email is already registered"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match."
        return errors

    def loginValidator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['noEmail'] = "Please input an email."
        elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', postData['email']):
            errors['emaiValid'] = "Email is not valid."
        elif not User.objects.get(email=postData['email']):
            errors['emailExist'] = "This email is not registered in our database."
        if len(postData['password']) < 1:
            errors['noPass'] = "Please input a password."
        elif bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()) == False:
            errors['incorrect_pass'] = "Incorrect password"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class WishManager(models.Manager):
    def wish_list_manager(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = 'Name must be at least 3 characters long'
            return errors


class Wishlist(models.Model):
    name = models.CharField(max_length=50)
    added_by = models.ForeignKey(User, related_name='created')
    created_at = models.DateTimeField(auto_now_add=True)
    liked_users = models.ManyToManyField(User, related_name='liked_items')

    objects = WishManager()
