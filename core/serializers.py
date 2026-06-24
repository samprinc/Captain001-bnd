from rest_framework import serializers
from .models import Service, PortfolioImage, Testimonial, Partner, Post, Booking, Subscriber, CaseStudy, CaseStudyMetric

class ServiceSerializer(serializers.ModelSerializer):
    # This turns the list of ID-linked deliverables into a clean list of strings
    deliverables = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'title', 'tagline', 'description', 'image', 'icon', 'deliverables']

class PortfolioImageSerializer(serializers.ModelSerializer):
    # This reaches across the Foreign Key and grabs the string name
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = PortfolioImage
        # Explicitly list the fields so React gets exactly what it needs
        fields = ['id', 'title', 'client', 'category_name', 'image', 'is_featured', 'uploaded_at']
        
    def get_image(self, obj):
        # We can use the same bulletproof trick here just in case!
        if not obj.image:
            return None
        img_str = str(obj.image)
        if 'http' in img_str:
            http_index = img_str.find('http')
            return img_str[http_index:]
        if hasattr(obj.image, 'url'):
            return obj.image.url
        return img_str

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    # Flattening related fields to match your React 'Post' type
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    
    # ==== SPRINT 3 FIX: Take control of the image field ====
    image = serializers.SerializerMethodField() 

    class Meta:
        model = Post
        fields = [
            'id','slug', 'title', 'excerpt', 'content', 'category_name', 
            'author_name', 'publish_at', 'read_time', 'image', 'tags'
        ]

   # ==== BULLETPROOF IMAGE HANDLER ====
    def get_image(self, obj):
        if not obj.image:
            return None
        
        img_str = str(obj.image)
        
        # 1. If there is an external link anywhere in the string, extract it cleanly
        # This catches "https://..." AND "image/upload/https://..."
        if 'http' in img_str:
            # Find where 'http' starts and return everything from that point onward
            http_index = img_str.find('http')
            return img_str[http_index:]
            
        # 2. If it is a normal local file uploaded via the Django Admin
        if hasattr(obj.image, 'url'):
            return obj.image.url
            
        return img_str


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'name', 'date_subscribed']
        read_only_fields = ['date_subscribed']


class CaseStudyMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyMetric
        fields = ['label', 'value']

class CaseStudySerializer(serializers.ModelSerializer):
    # This nests the metrics perfectly inside the CaseStudy JSON array
    metrics = CaseStudyMetricSerializer(many=True, read_only=True)

    class Meta:
        model = CaseStudy
        fields = [
            'id', 'title', 'slug', 'client_name', 'industry', 'project_type', 
            'challenge', 'solution', 'outcome', 'metrics', 'hero_image', 'featured'
        ]