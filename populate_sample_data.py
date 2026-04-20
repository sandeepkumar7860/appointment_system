#!/usr/bin/env python
import os
import django
import sys
from datetime import date, timedelta
from django.contrib.auth.models import User

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointment_booking.settings')
django.setup()

from appointments.models import Teacher, Appointment

def create_sample_data():
    # Create sample teachers
    teachers_data = [
        {'name': 'Dr. Sarah Johnson', 'subject': 'Mathematics', 'avatar_url': 'https://randomuser.me/api/portraits/women/1.jpg'},
        {'name': 'Prof. Michael Chen', 'subject': 'Physics', 'avatar_url': 'https://randomuser.me/api/portraits/men/2.jpg'},
        {'name': 'Ms. Emily Davis', 'subject': 'Chemistry', 'avatar_url': 'https://randomuser.me/api/portraits/women/3.jpg'},
        {'name': 'Dr. Robert Wilson', 'subject': 'Biology', 'avatar_url': 'https://randomuser.me/api/portraits/men/4.jpg'},
        {'name': 'Mrs. Lisa Anderson', 'subject': 'English Literature', 'avatar_url': 'https://randomuser.me/api/portraits/women/5.jpg'},
    ]

    teachers = []
    for teacher_data in teachers_data:
        teacher, created = Teacher.objects.get_or_create(
            name=teacher_data['name'],
            defaults={
                'subject': teacher_data['subject'],
                'avatar_url': teacher_data['avatar_url']
            }
        )
        teachers.append(teacher)
        if created:
            print(f"Created teacher: {teacher.name}")

    # Create a sample admin user if it doesn't exist
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Created admin user: admin (password: admin123)")

    # Create sample regular users
    users_data = [
        {'username': 'student1', 'email': 'student1@example.com'},
        {'username': 'student2', 'email': 'student2@example.com'},
        {'username': 'student3', 'email': 'student3@example.com'},
    ]

    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={'email': user_data['email']}
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {user.username}")
        users.append(user)

    # Create sample appointments
    import random
    from django.utils import timezone

    statuses = ['pending', 'granted', 'rejected']
    time_slots = ['8-9', '9-10', '10-11', '11-12']

    for i in range(20):
        user = random.choice(users)
        teacher = random.choice(teachers)
        appointment_date = date.today() + timedelta(days=random.randint(-7, 14))
        time_slot = random.choice(time_slots)
        status = random.choice(statuses)

        # Check if appointment already exists
        if not Appointment.objects.filter(
            user=user,
            teacher=teacher,
            date=appointment_date,
            time_slot=time_slot
        ).exists():
            appointment = Appointment.objects.create(
                user=user,
                teacher=teacher,
                date=appointment_date,
                time_slot=time_slot,
                status=status,
                message=f"Sample appointment {i+1}" if random.choice([True, False]) else ""
            )
            print(f"Created appointment: {appointment}")

    print("\nSample data creation completed!")
    print("Admin dashboard URL: http://127.0.0.1:8000/admin-dashboard/")
    print("Django Admin URL: http://127.0.0.1:8000/admin/")
    print("Login credentials:")
    print("  Admin: admin / admin123")
    print("  Students: student1, student2, student3 / password123")

if __name__ == '__main__':
    create_sample_data()