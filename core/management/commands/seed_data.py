from django.core.management.base import BaseCommand
from core.models import (
    Service, Partner, PortfolioImage, ServiceDeliverable, 
    Testimonial, CaseStudy, CaseStudyMetric,PortfolioCategory
)

class Command(BaseCommand):
    help = 'Seeds the database with premium agency data'

    def handle(self, *args, **kwargs):
        
        # 1. Seed Services
        if not Service.objects.exists():
            service1 = Service.objects.create(
                title="Cinematic Production",
                excerpt="Visual storytelling, engineered.",
                description="From concept to color grade. We produce commercial films, brand documentaries, and editorial visuals shot in 4K.",
                icon="fa-solid fa-clapperboard"
            )
            ServiceDeliverable.objects.create(service=service1, name="Brand Films & Commercials (4K / 6K)")
            ServiceDeliverable.objects.create(service=service1, name="Documentary & Editorial Shoots")
            
            service2 = Service.objects.create(
                title="Brand Architecture",
                excerpt="Identities built to outlast trends.",
                description="We design brand systems with the rigor of a magazine and the discipline of a tech platform.",
                icon="fa-solid fa-pen-nib"
            )
            ServiceDeliverable.objects.create(service=service2, name="Brand Strategy & Positioning")
            ServiceDeliverable.objects.create(service=service2, name="Visual Identity Systems")
            self.stdout.write(self.style.SUCCESS("Successfully seeded Services"))

        # 2. Seed Partners
        if not Partner.objects.exists():
            partners = ["Tesh Academy", "Global Connections", "Gucha Stars", "TAWUWU", "Northbound Coffee"]
            for p in partners:
                Partner.objects.create(name=p, logo="https://placehold.co/200x100")
            self.stdout.write(self.style.SUCCESS("Successfully seeded Partners"))

        # 3. Seed Portfolio
        if not PortfolioImage.objects.exists():
            # First, ensure the categories exist
            cat_moments, _ = PortfolioCategory.objects.get_or_create(name="Best Moments")
            cat_posters, _ = PortfolioCategory.objects.get_or_create(name="Posters")
            cat_samples, _ = PortfolioCategory.objects.get_or_create(name="Samples")

            # Now create the images, passing the OBJECT instance
            PortfolioImage.objects.create(
                title="Cinematic Documentary Shoot", 
                client_name="Northbound Coffee Co.", 
                location="Nairobi, Kenya",
                category=cat_moments, # Pass the object, not the string
                image="https://images.pexels.com/photos/3379934/pexels-photo-3379934.jpeg"
            )
            
            PortfolioImage.objects.create(
                title="Corporate Event Banner", 
                client_name="TAWUWU", 
                location="Nairobi, Kenya",
                category=cat_posters, # Pass the object, not the string
                image="https://images.pexels.com/photos/1701202/pexels-photo-1701202.jpeg"
            )
            self.stdout.write(self.style.SUCCESS("Successfully seeded Portfolio"))
            
        # 4. Seed Testimonials
        if not Testimonial.objects.exists():
            Testimonial.objects.create(
                author="Amani Otieno",
                role="Founder",
                company="Northbound Coffee Co.",
                quote="The visual identity Captain 001 built for us completely shifted our market position.",
                image=None
            )
            self.stdout.write(self.style.SUCCESS("Successfully seeded Testimonials"))

        # 5. Seed Case Studies
        if not CaseStudy.objects.exists():
            cs = CaseStudy.objects.create(
                title="Pan-African Financial Initiative",
                slug="pan-african-finance",
                client_name="Finance Corp",
                industry="Fintech",
                project_type="Brand Architecture",
                challenge="Low brand visibility across regional markets.",
                solution="Complete media strategy, production, and digital rollout.",
                outcome="Dominant brand authority and record-breaking engagement.",
                hero_image="https://images.unsplash.com/photo-1556761175-5973dc0f32e7",
                featured=True
            )
            # Add metrics to the case study
            CaseStudyMetric.objects.create(case_study=cs, value="3.4M", label="Impressions")
            CaseStudyMetric.objects.create(case_study=cs, value="+45%", label="Growth")
            
            self.stdout.write(self.style.SUCCESS("Successfully seeded Case Studies"))