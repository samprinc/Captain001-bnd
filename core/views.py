from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service, PortfolioImage, Testimonial, Partner, Post, Booking, Subscriber, CaseStudy
from .serializers import (
    ServiceSerializer, PortfolioImageSerializer, TestimonialSerializer,
    PartnerSerializer, PostSerializer, BookingSerializer, SubscriberSerializer, CaseStudySerializer
)
from .pagination import StandardResultsSetPagination
from rest_framework import generics

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    # OPTIMIZED: prefetch_related prevents N+1 queries for the deliverables list
    queryset = Service.objects.prefetch_related('deliverables').filter(is_active=True).order_by('id')
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    pagination_class = None  

class PortfolioImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PortfolioImage.objects.all().order_by('-uploaded_at')
    serializer_class = PortfolioImageSerializer
    permission_classes = [AllowAny]
    pagination_class = None

class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True).order_by('id')
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]
    pagination_class = None

class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Partner.objects.all().order_by('id')
    serializer_class = PartnerSerializer
    permission_classes = [AllowAny]
    pagination_class = None

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    # OPTIMIZED: select_related (ForeignKeys) and prefetch_related (ManyToMany) 
    # drops the database queries from ~40 down to exactly 3 per page load.
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags').filter(is_published=True).order_by('-publish_at')
    
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    pagination_class = StandardResultsSetPagination
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__name'] 
    
    # FIXED: Added __name to tags so Django searches the string, not the object
    search_fields = ['title', 'excerpt', 'content', 'tags__name'] 


# ==== SECURED SPRINT 3 UPGRADE ====
# Changed from ModelViewSet to GenericViewSet + CreateModelMixin.
# This ensures the public API can ONLY accept POST requests for new bookings,
# and will return a 405 Method Not Allowed if anyone tries to GET/steal the leads.
class BookingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.all().order_by('-booked_at')
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

class SubscriberCreateAPIView(generics.CreateAPIView):
    """
    Endpoint for the Magazine Mailing List.
    Allows public (AllowAny) POST requests to add a new subscriber.
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [AllowAny]  # Anyone visiting the site can subscribe


class CaseStudyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public endpoint to list and retrieve case studies.
    """
    queryset = CaseStudy.objects.all()
    serializer_class = CaseStudySerializer
    # Optional: allows React to fetch a specific case study via URL /api/case-studies/brand-launch/
    lookup_field = 'slug'