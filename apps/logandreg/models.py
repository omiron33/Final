from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self,postData):
        errors = {}
        ## Registration
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First Name can't be empty"
        elif len(postData['first_name']) < 3:
            errors['first_name1'] = "First Name must be greater than 2 characters"
        elif not postData['first_name'].isalpha():
            errors['first_namedig'] = "First name may not contain numbers or spaces"
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last Name can't be empty"
        elif len(postData['last_name']) < 3:
            errors['last_name1'] = "Last Name must be greater than 2 characters"
        elif not postData['last_name'].isalpha():
            errors['last_namedig'] = "Last name may not contain numbers or spaces"
        if len(postData['pw']) < 1:
            errors['pw_len'] = "Password field is empty"
        elif len(postData['pw']) < 8:
            errors['pw_len2'] = "Password is less than 8 characters"
        elif postData['pw'] != postData['confirm']:
             errors['pw'] = "Passwords do not match"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not a valid email address'
        return errors
    def login_validator(self,postData):
        errors = {}
        ## Login
        if not EMAIL_REGEX.match(postData['logEmail']):
            errors['email'] = 'Email is not a valid email address'
        if len(postData['logPW']) < 1:
            errors['pw_len'] = "Password field is empty"
        check = User.objects.filter(email = postData['logEmail'])
        if len(check) < 1:
            errors['login'] = "User does not exist"
        if not bcrypt.checkpw(postData['logPW'].encode(), check[0].password.encode()):
            errors['password'] = "Password is incorrect"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()