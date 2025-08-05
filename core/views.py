from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, filters, generics, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


from .models import (
    Service, Post, Comment, Booking, Advertisement, Partner, Author,
    Category, Tag, Subscriber, NewsletterSubscriber, AdView, AdClick, Event
)
from .serializers import (
    ServiceSerializer, PostSerializer, CommentSerializer,
    BookingSerializer, AdvertisementSerializer, PartnerSerializer,
    AuthorSerializer, CategorySerializer, TagSerializer,
    SubscriberSerializer, NewsletterSubscriberSerializer, EventSerializer
)

# =======================
# ✅ ADS ANALYTICS API
# =======================

@api_view(['GET'])
def ad_stats(request):
    today = timezone.now().date()
    ads = Advertisement.objects.filter(
        active=True, start_date__lte=today, end_date__gte=today
    )
    stats = []

    for ad in ads:
        views = ad.views.count()
        clicks = ad.clicks.count()
        ctr = round((clicks / views) * 100, 2) if views else 0

        stats.append({
            "id": ad.id,
            "title": ad.title,
            "placement": ad.placement,
            "device_target": ad.device_target,
            "views": views,
            "clicks": clicks,
            "ctr": ctr,
        })

    return Response(stats)

# =======================
# ✅ VIEWSETS
# =======================
class EventViewSet(viewsets.ReadOnlyModelViewSet):  # Only GET allowed
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer

class AdvertisementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdvertisementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        today = timezone.now().date()
        qs = Advertisement.objects.filter(active=True, start_date__lte=today, end_date__gte=today)

        placement = self.request.query_params.get('placement')
        device = self.request.query_params.get('device')

        if placement:
            qs = qs.filter(placement=placement)
        if device:
            qs = qs.filter(device_target__in=['both', device])

        return qs

    @action(detail=True, methods=["post"])
    def view(self, request, pk=None):
        ad = get_object_or_404(Advertisement, pk=pk)
        AdView.objects.create(
            ad=ad,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return Response({"message": "View tracked"}, status=200)

    @action(detail=True, methods=["post"])
    def click(self, request, pk=None):
        ad = get_object_or_404(Advertisement, pk=pk)
        AdClick.objects.create(
            ad=ad,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return Response({"message": "Click tracked"}, status=200)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

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
    filterset_fields = ['category', 'category__name', 'tags', 'tags__name']
    ordering_fields = ['publish_at']

    def get_queryset(self):
        if self.request.method == 'GET':
            return Post.objects.filter(
                is_published=True, publish_at__lte=timezone.now()
            ).order_by('-publish_at')
        return Post.objects.all().order_by('-publish_at')

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # Optional: allow anyone to post comments

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
class NewsletterSubscriberViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer

# =======================
# ✅ BASIC LIST VIEWS
# =======================

class PartnerList(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class SubscriberListCreateView(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
