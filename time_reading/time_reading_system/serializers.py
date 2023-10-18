from rest_framework import serializers
from time_reading_system.models import Book, SessionReading, UserProfile


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year_of_published', 'short_description']


class BookSerializer(serializers.ModelSerializer):
    full_time = serializers.TimeField()

    class Meta:
        model = Book
        fields = ['title', 'author', 'year_of_published', 'short_description', 'full_description', 'full_time']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionReading
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
