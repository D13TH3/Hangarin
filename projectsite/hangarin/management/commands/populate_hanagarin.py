import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from hangarin.models import Priority, Category, Task, Note, SubTask

class Command(BaseCommand):
    help = 'Populates the Hangarin database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        self.stdout.write("Generating fake data...")

        # 1. Get existing Priorities and Categories (Make sure you added them in Admin first!)
        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        if not priorities or not categories:
            self.stdout.write(self.style.ERROR("Please add Priorities and Categories in Admin first!"))
            return

        # 2. Generate 20 Tasks
        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5), # Requirement: sentence()
                description=fake.paragraph(nb_sentences=3), # Requirement: paragraph()
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]), # Requirement: random_element()
                priority=random.choice(priorities),
                category=random.choice(categories)
            )

            # 3. Generate a Note for each Task
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2)
            )

            # 4. Generate 2 SubTasks for each Task
            for _ in range(2):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=3),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated 20 Tasks, 20 Notes, and 40 SubTasks!"))
