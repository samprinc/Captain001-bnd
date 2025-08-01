from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service, Post, Comment, Booking, Advertisement, Partner, Author, Category, Tag, Subscriber, NewsletterSubscriber
from rest_framework import generics
from .serializers import *
from django.utils import timezone



class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all() 
    serializer_class = AuthorSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['category', 'tags']
    ordering_fields = ['publish_at']
    filterset_fields = ['category', 'category__name', 'tags', 'tags__name']


    def get_queryset(self):
        if self.request.method == 'GET':
            return Post.objects.filter(
                is_published=True,
                publish_at__lte=timezone.now()
            ).order_by('-publish_at')
        return Post.objects.all().order_by('-publish_at')
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-booked_at')
    serializer_class = BookingSerializer

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.filter(active=True)
    serializer_class = AdvertisementSerializer

class PartnerList(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class SubscriberListCreateView(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

# views.py
class NewsletterSubscriberViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
