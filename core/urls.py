# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceViewSet, PortfolioImageViewSet, SubscriberCreateAPIView, TestimonialViewSet,
    PartnerViewSet, PostViewSet, BookingViewSet, 
    CaseStudyViewSet  # <-- Import it here
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'portfolio', PortfolioImageViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'partners', PartnerViewSet)
router.register(r'posts', PostViewSet)
router.register(r'bookings', BookingViewSet)

# 🚀 Register the Case Studies endpoint
router.register(r'case-studies', CaseStudyViewSet, basename='casestudy')

urlpatterns = [
    path('', include(router.urls)),
    path('subscribers/', SubscriberCreateAPIView.as_view(), name='subscriber-create'),
]