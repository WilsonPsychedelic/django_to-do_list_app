from django.conf import settings
from django.db import models


class Category(models.Model):
    name  = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
    )

    def __str__(self):
        return self.name


class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
    ]

    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed   = models.BooleanField(default=False)
    priority    = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')
    due_date    = models.DateField(null=True, blank=True)
    category    = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='todos',
    )
    owner       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='todos',
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title