from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = CloudinaryField('icon', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    profile_pic = CloudinaryField("image", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    image = CloudinaryField("image", blank=True, null=True)
    content = CKEditor5Field("Content")  # Use Rich Text field
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_published = models.BooleanField(default=False)
    publish_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} on {self.post.title}"


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service.title}"


class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    link = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = CloudinaryField('logo')
    link = models.URLField()

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
