from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ServiceViewSet, PostViewSet, CommentViewSet, BookingViewSet, 
    AdvertisementViewSet, AuthorViewSet, CategoryViewSet, TagViewSet,
    PartnerList, SubscriberListCreateView, NewsletterSubscriberViewSet, 
    EventViewSet,
    ad_stats  # ✅ import ad_stats
)

router = DefaultRouter()
router.register('services', ServiceViewSet)
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet)
router.register('bookings', BookingViewSet)
router.register('promotions', AdvertisementViewSet, basename='advertisement')
router.register('authors', AuthorViewSet, basename='author')
router.register('categories', CategoryViewSet, basename='category')
router.register('tags', TagViewSet, basename='tag')
router.register('newsletter', NewsletterSubscriberViewSet)
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
    path('partners/', PartnerList.as_view(), name='partner-list'),
    path('subscribers/', SubscriberListCreateView.as_view(), name='subscriber-list-create'),
    path('ad-stats/', ad_stats, name='ad-stats'),  # ✅ analytics endpoint
]
