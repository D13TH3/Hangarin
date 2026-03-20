📋 Hangarin (Task Management System)
Hangarin is a modern, high-contrast Task Management Dashboard built with Django. It helps students and professionals organize their daily goals with subtasks, category filtering, and real-time efficiency tracking.
✨ Features
Social Authentication: Secure login using Google and GitHub via django-allauth.
Dynamic Dashboard:
Total Tasks: Tracks your current workload.
Victory Card: Displays your completion count and a calculated Efficiency Score.
Due Soon: Alerts you to tasks with deadlines within the next 48 hours.
Task Management:
Subtasks: Break down big goals into smaller steps.
Notes: Add sticky-note style details to any task.
Priority & Categories: Color-coded badges for better organization.
Search & Filter: Quickly find tasks by title or filter by specific categories.
Modern UI: High-contrast dark theme with a sticky footer and responsive Bootstrap cards.
🛠️ Tech Stack
Backend: Django 5.x
Frontend: Bootstrap 5, MDB (Material Design for Bootstrap), FontAwesome Icons
Database: SQLite (Development)
Auth: Django-allauth (OAuth2)
Fake Data: Faker (for database population)

🚀 Getting Started
1. Clone the repository
git clone https://github.com
cd hangarin
2. Install Dependencies
pip install django django-allauth django-widget-tweaks faker
3. Setup Database
python manage.py makemigrations
python manage.py migrate
4. Create a Superuser
python manage.py createsuperuser
5. Populate with Demo Data (Optional)
python manage.py populate_hangarin
6. Run the Server
python manage.py runserver

