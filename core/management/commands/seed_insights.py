from django.core.management.base import BaseCommand
from core.models import Author, Category, Tag, Post

class Command(BaseCommand):
    help = 'Seeds the database with Insights and Magazine articles'

    def handle(self, *args, **kwargs):
        # 1. Setup the Master Author
        author, _ = Author.objects.get_or_create(
            name="Stephen Ndemo Jr.",
            defaults={
                "email": "stephenndemo55@gmail.com",
                "bio": "Founder & Creative Director at Captain 001 Media."
            }
        )

        # 2. The Core Editorial Content (From your React frontend)
        long_body = """
        <p>The work of building a brand has never been louder, and yet rarely has it felt more quiet. The discipline now lives in the gap between what a company says and what a culture is willing to repeat about it. That gap is the entire job.</p>
        <p>We design for that gap. We write for it. We film for it. The brands that move in the next decade will not be the ones with the loudest channels — they will be the ones with the cleanest signal.</p>
        <p>Editorial thinking is the unlock. Treat every touchpoint like a cover story: a clear point of view, a single visual idea, a sentence a stranger could repeat at dinner. When the work survives a reader's attention, it survives the algorithm.</p>
        <p>The studios doing this well are quietly rewriting what "agency" means. Less deck, more direction. Less performance, more press. Less brand book, more body of work.</p>
        """

        posts_data = [
            {
                "title": "Editorial Is the New Marketing",
                "excerpt": "Why the brands of the next decade will be built like magazines — and run like newsrooms.",
                "category": "Brand Strategy",
                "read_time": 7,
                # Added &fake=.jpg to trick Django's file extension logic
                "image": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1800&q=80&fake=.jpg",
                "tags": ["Editorial", "Strategy", "Brand"]
            },
            {
                "title": "The Quiet Power of Monochrome",
                "excerpt": "Color is loud. Restraint is louder. A field note on designing identities that age in public.",
                "category": "Design",
                "read_time": 5,
                "image": "https://images.unsplash.com/photo-1600132806370-bf17e65e942f?auto=format&fit=crop&w=1800&q=80&fake=.jpg",
                "tags": ["Design", "Identity"]
            },
            {
                "title": "Press Is a Product",
                "excerpt": "Stop pitching. Start packaging. The new mechanics of earning a Tier-1 placement.",
                "category": "Digital PR",
                "read_time": 6,
                "image": "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?auto=format&fit=crop&w=1800&q=80&fake=.jpg",
                "tags": ["PR", "Media"]
            },
            {
                "title": "The Shot List Is a Strategy Document",
                "excerpt": "How production planning quietly decides whether a brand film actually moves a market.",
                "category": "Production",
                "read_time": 8,
                "image": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=1800&q=80&fake=.jpg",
                "tags": ["Production", "Film"]
            },
            {
                "title": "Founders Belong on the Cover",
                "excerpt": "Why executive profiling outperforms paid acquisition in the trust economy.",
                "category": "Digital PR",
                "read_time": 5,
                "image": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1800&q=80&fake=.jpg",
                "tags": ["PR", "Founders"]
            },
            {
                "title": "Typography Is Architecture",
                "excerpt": "A field note on building identities that read like buildings stand.",
                "category": "Design",
                "read_time": 4,
                "image": "https://images.unsplash.com/photo-1561089489-02ba252b414f?auto=format&fit=crop&w=1800&q=80&fake=.jpg",
                "tags": ["Typography", "Design"]
            },
            {
                "title": "Run Your Brand Like a Newsroom",
                "excerpt": "Editorial calendars, beats, and the org chart shift no marketing team is talking about.",
                "category": "Brand Strategy",
                "read_time": 6,
                "image": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1800&q=80&fake=.jpg",
                "tags": ["Strategy", "Editorial"]
            },
            {
                "title": "Kenya Is a Creative Export",
                "excerpt": "Notes from Nairobi on why East African studios are quietly reshaping global production.",
                "category": "Industry",
                "read_time": 7,
                "image": "https://images.unsplash.com/photo-1547471080-7fc2caa6c154?auto=format&fit=crop&w=1800&q=80&fake=.jpg",
                "tags": ["Industry", "Nairobi"]
            }
        ]

        # 3. Inject the Data
        for data in posts_data:
            # Check if post already exists so we don't duplicate
            if not Post.objects.filter(title=data['title']).exists():
                
                # Get or Create Category
                category_obj, _ = Category.objects.get_or_create(name=data['category'])
                
                # Create the Post
                post = Post.objects.create(
                    title=data['title'],
                    excerpt=data['excerpt'],
                    content=long_body,
                    category=category_obj,
                    author=author,
                    read_time=data['read_time'],
                    image=data['image'],
                    is_published=True  # Ensure it shows up on the frontend instantly
                )

                # Attach Tags
                for tag_name in data['tags']:
                    tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag_obj)

        self.stdout.write(self.style.SUCCESS("Successfully seeded the Insights Magazine!"))