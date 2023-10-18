from django.urls import path, include, re_path
from time_reading_system.views import BooksAPI, BookAPI, ReadingSessionList, ReadingSessionDetail, UserAPI

urlpatterns = [
    path('book/', BooksAPI.as_view(), name='books-list'),
    re_path(r'^book/(?P<book_id>\d+)/$', BookAPI.as_view(), name='book-detail'),
    path('sessions/', ReadingSessionList.as_view(), name='reading-session-list'),
    re_path(r'^sessions/(?P<sess_id>\d+)/$', ReadingSessionDetail.as_view(), name='reading-session-detail'),
    path('drf-auth', include('rest_framework.urls')),

    path('user/', UserAPI.as_view(), name='user'),
]
