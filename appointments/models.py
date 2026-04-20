from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    avatar_url = models.URLField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    TIME_SLOTS = [
        ('8-9', '8-9'),
        ('9-10', '9-10'),
        ('10-11', '10-11'),
        ('11-12', '11-12'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('granted', 'Granted'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time_slot = models.CharField(max_length=10, choices=TIME_SLOTS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.teacher.name} - {self.date} {self.time_slot}"
