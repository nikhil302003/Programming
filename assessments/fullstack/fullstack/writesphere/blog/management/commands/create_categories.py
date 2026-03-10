from django.core.management.base import BaseCommand
from blog.models import Category

class Command(BaseCommand):
    help = 'Create sample categories for the blog'

    def handle(self, *args, **options):
        categories_data = [
            {
                'name': 'Technology',
                'slug': 'technology',
                'description': 'Posts about technology, programming, and software development'
            },
            {
                'name': 'Lifestyle',
                'slug': 'lifestyle',
                'description': 'Posts about lifestyle, personal development, and wellness'
            },
            {
                'name': 'Travel',
                'slug': 'travel',
                'description': 'Posts about travel, adventures, and exploring new places'
            },
            {
                'name': 'Business',
                'slug': 'business',
                'description': 'Posts about business, entrepreneurship, and career development'
            },
            {
                'name': 'Education',
                'slug': 'education',
                'description': 'Posts about education, learning, and academic topics'
            }
        ]

        created_count = 0
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                slug=cat_data['slug'],
                description=cat_data['description']
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {category.name}"))

        self.stdout.write(self.style.SUCCESS(f"Categories setup completed! Created {created_count} new categories."))
