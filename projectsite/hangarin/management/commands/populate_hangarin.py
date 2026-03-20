import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User # Required
from faker import Faker
from hangarin.models import Priority, Category, Task, Note, SubTask

class Command(BaseCommand):
    help = 'Populates the Hangarin database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Get your admin/login user to "own" the tasks
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("Create a superuser first!"))
            return

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        if not priorities or not categories:
            self.stdout.write(self.style.ERROR("Add Priorities and Categories in Admin first!"))
            return

        self.stdout.write(f"Generating 20 tasks for {user.username}...")

        for _ in range(20):
            task = Task.objects.create(
                user=user, # Link the task to the user
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                priority=random.choice(priorities),
                category=random.choice(categories)
            )

            Note.objects.create(task=task, content=fake.paragraph(nb_sentences=2))
            for _ in range(2):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=3),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
                )

        self.stdout.write(self.style.SUCCESS(f"Done! Created 20 tasks for {user.username}"))
