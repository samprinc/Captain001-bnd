from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ServiceViewSet, PostViewSet, CommentViewSet, BookingViewSet,
    AdvertisementViewSet, AuthorViewSet, CategoryViewSet, TagViewSet,
    PartnerList, SubscriberListCreateView, NewsletterSubscriberViewSet
)

router = DefaultRouter()
router.register('services', ServiceViewSet)
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet)
router.register('bookings', BookingViewSet)
router.register('promotions', AdvertisementViewSet)
router.register('authors', AuthorViewSet, basename='author')
router.register('categories', CategoryViewSet, basename='category')
router.register('tags', TagViewSet, basename='tag')
# urls.py
router.register('newsletter', NewsletterSubscriberViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('partners/', PartnerList.as_view(), name='partner-list'),
    path('subscribers/', SubscriberListCreateView.as_view(), name='subscriber-list-create'),
]
