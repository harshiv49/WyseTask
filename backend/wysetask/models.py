from django.db import models
# Create a new user
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
class User(AbstractUser):
    username=models.CharField(max_length=100,null=True,blank=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    email=models.EmailField(unique=True,max_length=100)
    mobile=models.CharField(max_length=14,default=0000000000)
    is_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    forget_password=models.CharField(max_length=100,null=True,blank=True)
    last_login_time=models.DateTimeField(null=True,blank=True)
    last_logout_time=models.DateTimeField(null=True,blank=True)
    objects=UserManager()
    auth_provider = models.CharField(
        max_length=50, blank=True, default='email')
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

