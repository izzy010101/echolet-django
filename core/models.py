
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser



# Custom User Model
class User(AbstractUser):
    email_verified_at = models.DateTimeField(null=True, blank=True)
    theme_color = models.CharField(max_length=20, default='blue')

    REQUIRED_FIELDS = ['email']

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Post Model
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField()
    body = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



