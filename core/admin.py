from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget  # ✅ Correct import

from .models import ActiveOffer,Engagement,Service, Post, Comment, Booking, Advertisement, Partner, Subscriber, Author, Category, Tag, NewsletterSubscriber, AdView, AdClick, Event

admin.site.site_header = "Captain Media Admin"
admin.site.site_title = "Captain Media Admin Portal"
admin.site.index_title = "Welcome to Captain Media Dashboard"

# Custom form to use CKEditor5 in admin
class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='default')  # ✅ Applies CKEditor5 widget to `content` field
        }
# admin.py

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'placement',
        'device_target',
        'start_date',
        'end_date',
        'active',
        'total_views',
        'total_clicks',
        'ctr',
    )
    list_filter = ('active', 'device_target', 'placement', 'start_date', 'end_date')
    search_fields = ('title',)

    def total_views(self, obj):
        return obj.views.count()

    def total_clicks(self, obj):
        return obj.clicks.count()

    def ctr(self, obj):
        views = obj.views.count()
        clicks = obj.clicks.count()
        return f"{(clicks / views * 100):.2f}%" if views else "0.00%"

@admin.register(AdView)
class AdViewAdmin(admin.ModelAdmin):
    list_display = ('ad', 'ip_address', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('ip_address',)

@admin.register(AdClick)
class AdClickAdmin(admin.ModelAdmin):
    list_display = ('ad', 'ip_address', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('ip_address',)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ("title", "publish_at", "is_published")
    list_filter = ("publish_at",)
    search_fields = ("title", "content")

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'date_subscribed')
    search_fields = ('email', 'name')

# Register other models
admin.site.register(Partner)
   
admin.site.register(Service)
admin.site.register(Comment)
admin.site.register(Booking)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(NewsletterSubscriber)
admin.site.register(Engagement)
admin.site.register(ActiveOffer)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location')
    ordering = ('date',)



