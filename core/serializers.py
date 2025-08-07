from rest_framework import serializers
from .models import (
    Service, Post, Comment, Booking, Advertisement,
    Partner, Subscriber, Author, Category, Tag, NewsletterSubscriber, Event, Engagement, ActiveOffer
)

import re

# === Author / Category / Tag ===
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'profile_pic', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


# === Comments / Posts ===

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'image', 'content', 'author',
            'category', 'tags', 'is_published', 'publish_at', 'comments'
        ]



# === Services / Bookings ===

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate_phone(self, value):
        if not re.match(r'^\+?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value

# === Ads ===

class AdvertisementSerializer(serializers.ModelSerializer):
    views_count = serializers.IntegerField(source='views.count', read_only=True)
    clicks_count = serializers.IntegerField(source='clicks.count', read_only=True)
    is_live = serializers.SerializerMethodField()
    ctr = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = '__all__'

    def get_is_live(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        return obj.active and obj.start_date <= today <= obj.end_date

    def get_ctr(self, obj):
        views = obj.views.count()
        clicks = obj.clicks.count()
        return round((clicks / views) * 100, 2) if views else 0


# === Partner / Subscriber ===

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']



class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engagement
        fields = '__all__'

# backend/news/serializers.py


class ActiveOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveOffer
        fields = ['id', 'title', 'expires', 'link']
