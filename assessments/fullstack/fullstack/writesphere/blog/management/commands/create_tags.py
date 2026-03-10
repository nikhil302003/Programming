from django.core.management.base import BaseCommand
from blog.models import Tag

class Command(BaseCommand):
    help = 'Create sample tags for the blog'

    def handle(self, *args, **options):
        tags_data = [
            'Python',
            'Django',
            'Web Development',
            'JavaScript',
            'React',
            'Machine Learning',
            'Data Science',
            'Travel',
            'Photography',
            'Food',
            'Health',
            'Fitness',
            'Business',
            'Marketing',
            'Education',
            'Technology',
            'Programming',
            'Tutorial',
            'Tips',
            'Lifestyle',
            'Personal Development'
        ]

        created_count = 0
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                slug=tag_name.lower().replace(' ', '-')
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created tag: {tag.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Tag already exists: {tag.name}"))

        self.stdout.write(self.style.SUCCESS(f"Tags setup completed! Created {created_count} new tags."))
