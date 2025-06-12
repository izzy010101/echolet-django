from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from core.models import User, Category, Post
import random
import string
from random import choice

class Command(BaseCommand):
    help = 'Seed database with demo user, categories, and posts'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding user, categories, and posts...")

        # Create demo user
        user, created = User.objects.get_or_create(
            email='demo@example.com',
            defaults={
                'username': 'demo',
                'password': 'pbkdf2_sha256$260000$fakehash',
                'theme_color': 'blue',
            }
        )
        if created:
            user.set_password('password')
            user.save()
            self.stdout.write("Created demo user.")
        else:
            self.stdout.write("ℹ️ Demo user already exists.")

        existing_categories = set(Category.objects.filter(user=user).values_list('name', flat=True))
        categories = ['Tech', 'Design', 'Wellness', 'Startups', 'Leadership']

        for name in categories:
            if name not in existing_categories:
                Category.objects.create(name=name, user=user)
        self.stdout.write("Categories seeded.")

        # Create 10 posts for the demo user
        if Post.objects.filter(user=user).count() == 0:
            available_categories = list(Category.objects.filter(user=user))

            for i in range(10):
                title = f"Sample Post {i + 1}"
                Post.objects.create(
                    user=user,
                    title=title,
                    category=choice(available_categories) if available_categories else None,
                    slug=slugify(title + '-' + ''.join(random.choices(string.ascii_lowercase, k=5))),
                    excerpt=f"This is a sample excerpt for post {i + 1}",
                    body="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum.",
                    published_at=timezone.now()
                )
            self.stdout.write("10 posts created.")
        else:
            self.stdout.write("ℹ️ Posts already exist.")
