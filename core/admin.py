from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Service, ServiceDeliverable, PortfolioImage, Testimonial, 
    Partner, Author, Category, Tag, Post, Booking, Subscriber
)

def admin_image_preview(obj):
    if hasattr(obj, 'image') and obj.image:
        return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
    return "No Image"
admin_image_preview.short_description = 'Preview'

# ==========================================
# 2. SERVICES & DELIVERABLES
# ==========================================

class ServiceDeliverableInline(admin.TabularInline):
    model = ServiceDeliverable
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)
    inlines = [ServiceDeliverableInline]

@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = (admin_image_preview, 'title', 'client', 'category', 'is_featured')
    list_editable = ('is_featured',)
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'client')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'role', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('author', 'quote')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', admin_image_preview)

# ==========================================
# 3. EDITORIAL / INSIGHTS HUB (Fixed)
# ==========================================

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',) # 🚀 Added search_fields to fix the autocomplete error

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', admin_image_preview, 'category', 'author', 'is_published', 'publish_at')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category', 'tags')
    search_fields = ('title', 'excerpt')
    list_select_related = ('author', 'category')
    autocomplete_fields = ('author', 'category') 
    date_hierarchy = 'publish_at'

# ==========================================
# 4. LEADS & CONVERSIONS (Fixed)
# ==========================================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # 🚀 Added 'status' to list_display so it can be edited
    list_display = ('name', 'service_requested', 'budget', 'status', 'status_colored', 'booked_at')
    list_editable = ('status',)
    list_filter = ('status', 'budget')
    search_fields = ('name', 'email', 'phone', 'service_requested')
    readonly_fields = ('booked_at',)
    date_hierarchy = 'booked_at'

    def status_colored(self, obj):
        colors = {'pending': 'orange', 'contacted': 'blue', 'proposal': 'purple', 'won': 'green', 'lost': 'red'}
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.status.upper()
        )
    status_colored.short_description = 'Status Label'

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'date_subscribed')
    search_fields = ('email', 'name')
    date_hierarchy = 'date_subscribed'

# core/admin.py (add to the bottom)
from .models import CaseStudy, CaseStudyMetric

class CaseStudyMetricInline(admin.TabularInline):
    model = CaseStudyMetric
    extra = 2 # Shows 2 empty metric rows by default

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'industry', 'featured')
    list_editable = ('featured',)
    list_filter = ('industry', 'project_type', 'featured')
    search_fields = ('title', 'client_name')
    prepopulated_fields = {'slug': ('title',)} # Auto-generates the slug as you type the title
    inlines = [CaseStudyMetricInline] # Injects the metrics builder