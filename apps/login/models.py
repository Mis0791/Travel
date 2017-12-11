from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+[\w]')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        if len(self.filter(username=post_data['username'])) > 0:
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('** Password Incorrect **')
        else:
            errors.append('** Username Incorrect **')
        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['name']) < 2: 
            errors.append("name field must be at least 3 characters")
        # #Check length of username
        if len(post_data['username']) < 2:
            errors.append("username field must be at least 3 characters")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        # check name fields for letter characters            
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('name field must be letter characters only')
        # check username
        if not re.match(USERNAME_REGEX, post_data['username']):
            errors.append("invalid username")
        # check uniqueness of username
        if len(User.objects.filter(username=post_data['username'])) > 0:
            errors.append("username already in use")
        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        # check uniqueness of email
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        # check password == password_confirm
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")

        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                username=post_data['username'],
                email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
