from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.utils.text import slugify

# ==========================================
# 1. CORE AGENCY SERVICES
# ==========================================

class Service(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, help_text="Short teaser for the service card")
    description = models.TextField()
    excerpt = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class (e.g., 'fa-video')")
    image = CloudinaryField('image', blank=True, null=True, help_text="Large cinematic image for the Services page")
    
    # Index added for efficient filtering on active homepage services
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.title


class ServiceDeliverable(models.Model):
    """Maps to the specific bullet points (features) inside the Service cards"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="deliverables")
    name = models.CharField(max_length=150, help_text="e.g., '4K Drone Cinematography'")

    def __str__(self):
        return f"{self.service.title} - {self.name}"


# ==========================================
# 2. PORTFOLIO, CLIENTS & SOCIAL PROOF
# ==========================================

# 1. NEW MODEL: Dynamic Categories
class PortfolioCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name_plural = "Portfolio Categories"

    def __str__(self):
        return self.name

class PortfolioImage(models.Model):
    """For the 'Selected Works' and full Gallery page"""
    title = models.CharField(max_length=100, blank=True, help_text="e.g., Cinematic Documentary Shoot")
    client = models.CharField(max_length=100, blank=True, help_text="e.g., Northbound Coffee Co.")
    location = models.CharField(max_length=200, blank=True, null=True)
    # 2. UPDATED: Now a ForeignKey pointing to the new model!
    category = models.ForeignKey(PortfolioCategory, on_delete=models.SET_NULL, null=True, blank=True)
    client_name = models.CharField(max_length=200, blank=True, null=True)
    image = CloudinaryField('image')
    is_featured = models.BooleanField(default=False, db_index=True, help_text="Show on the homepage grid?")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.title}"

class Testimonial(models.Model):
    """Client Experiences displayed on Gallery and Homepage"""
    author = models.CharField(max_length=100, help_text="e.g., Amani Otieno")
    role = models.CharField(max_length=100, help_text="e.g., Founder, Northbound Coffee")
    quote = models.TextField()
    company = models.CharField(max_length=100, blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    # Index added for filtering active recommendations
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"Testimonial from {self.author}"


class Partner(models.Model):
    """For the Marquee Trusted Brands section"""
    name = models.CharField(max_length=100)
    logo = CloudinaryField('logo', help_text="Upload a clean PNG with a transparent background")
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# ==========================================
# 3. EDITORIAL / INSIGHTS HUB (The Magazine)
# ==========================================

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    profile_pic = CloudinaryField("image", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    excerpt = models.TextField(help_text="Short summary for the article card", max_length=300)
    image = CloudinaryField("image", blank=True, null=True)
    
    # unique=True automatically builds a database index on the slug field
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    content = CKEditor5Field("Content")  
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    # NOTE: Keep an eye on this field at high-traffic scales. 
    # If concurrent writes cause locks, offload view tracking to Redis or a tracking pixel.
    views = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated read time in minutes")
    
    # Index added for instantaneous live article querying
    is_published = models.BooleanField(default=False, db_index=True)
    
    # Changed from auto_now_add=True to default=timezone.now so drafts can be pre-dated or updated correctly
    publish_at = models.DateTimeField(default=timezone.now, help_text="The date and time the post goes live")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ==========================================
# 4. LEADS & CONVERSIONS
# ==========================================

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('contacted', 'Discovery Call Scheduled'),
        ('proposal', 'Proposal Sent'),
        ('won', 'Closed Won'),
        ('lost', 'Closed Lost'),
    ]

    BUDGET_CHOICES = [
        ('Under Ksh 5k', 'Under Ksh 5k'),
        ('Ksh 5k - 20k', 'Ksh 5k - 20k'),
        ('Ksh 20k - 50k', 'Ksh 20k - 50k'),
        ('Ksh 5k - 150k', 'Ksh 50k - 150k'),
        ('Ksh 150k - 500k', 'Ksh 150k - 500k'),
        ('Ksh 500k+', 'Ksh 500k+'),
    ]

    # Storing service as a CharField protects historical analytics from cascade deletions
    service_requested = models.CharField(max_length=100) 
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    budget = models.CharField(max_length=50, choices=BUDGET_CHOICES)
    details = models.TextField(help_text="The client's project vision")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_requested} ({self.budget})"


class Subscriber(models.Model):
    """The Magazine Mailing List"""
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
# core/models.py (add to the bottom)

class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="URL friendly name (e.g., brand-launch)")
    client_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    project_type = models.CharField(max_length=100, help_text="e.g., Cinematic Production, Branding")
    
    challenge = models.TextField()
    solution = models.TextField()
    outcome = models.TextField()
    
    # Assuming you are using Cloudinary from earlier, otherwise use models.ImageField
    hero_image = models.ImageField(upload_to='case_studies/') 
    featured = models.BooleanField(default=False, help_text="Show this as the massive hero case study")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Case Studies"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class CaseStudyMetric(models.Model):
    """The dynamic numbers to show proof (e.g., 3.4M Impressions)"""
    case_study = models.ForeignKey(CaseStudy, related_name='metrics', on_delete=models.CASCADE)
    value = models.CharField(max_length=50, help_text="e.g., 3.4M or +45%")
    label = models.CharField(max_length=100, help_text="e.g., Impressions or Audience Growth")

    def __str__(self):
        return f"{self.value} {self.label}"