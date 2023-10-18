from django.contrib import admin

from time_reading_system.models import Book, SessionReading, UserProfile


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year_of_published']
    list_filter = ['author', 'year_of_published']


admin.site.register(Book, BookAdmin)


class SessionReadingAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'start_reading', 'end_reading', 'date_end_reading']
    list_filter = ['book', 'date_end_reading']


admin.site.register(SessionReading, SessionReadingAdmin)


class SessionReadingAdmin(admin.ModelAdmin):
    list_display = ['user', 'seven_day_time_reading', 'thirty_day_time_reading']


admin.site.register(UserProfile, SessionReadingAdmin)
