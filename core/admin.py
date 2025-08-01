from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget  # ✅ Correct import

from .models import Service, Post, Comment, Booking, Advertisement, Partner, Subscriber, Author, Category, Tag, NewsletterSubscriber

# Custom form to use CKEditor5 in admin
class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='default')  # ✅ Applies CKEditor5 widget to `content` field
        }

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
admin.site.register(Advertisement)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(NewsletterSubscriber)


