from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=32)
    second_name = models.CharField(max_length=64)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.role or 'No role'}"


class Task(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=248)
    unit = models.ManyToManyField(Unit, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status is None:
            try:
                self.status = Status.objects.get(name='Untouched')
            except Status.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} {self.status}'
