from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year_of_published = models.PositiveIntegerField()
    short_description = models.TextField()
    full_description = models.TextField()

    def __str__(self):
        return str(self.title)


class SessionReading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_reading = models.TimeField()
    end_reading = models.TimeField(null=True, blank=True)
    date_end_reading = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.book)

    class Meta:
        ordering = ['date_end_reading']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    seven_day_time_reading = models.TimeField(null=True, blank=True)
    thirty_day_time_reading = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


