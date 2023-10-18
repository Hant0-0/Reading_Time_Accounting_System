import datetime
from datetime import datetime as date
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from time_reading_system.models import Book, SessionReading, UserProfile
from time_reading_system.serializers import BooksSerializer, SessionSerializer, BookSerializer, UserSerializer
from time_reading_system.tasks import statistics_total_reading_time, counting_full_time_reading


class BooksAPI(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BooksSerializer(books, many=True).data
        return Response(serializer)


class BookAPI(APIView):
    def get(self, request, book_id=None):
        try:
            book = get_object_or_404(Book, id=book_id)
            all_reading_time = SessionReading.objects.filter(book=book, end_reading__isnull=False)

            book_data = {
                'title': book.title,
                'author': book.author,
                'year_of_published': book.year_of_published,
                'short_description': book.short_description,
                'full_description': book.full_description,
                'full_time': counting_full_time_reading(all_reading_time)
            }

            serializer = BookSerializer(data=book_data)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReadingSessionList(generics.ListCreateAPIView):

    queryset = SessionReading.objects.all()
    serializer_class = SessionSerializer

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        user = request.user

        """ Перевірка, чи користувач завершив попередню сесію """
        active_sessions = SessionReading.objects.filter(user=user, book_id=book_id, end_reading__isnull=True)
        if active_sessions.exists():
            return Response({'detail': 'Завершіть поточну сесію читання перед початком нової.'},
                            status=status.HTTP_400_BAD_REQUEST)

        """ Завершення попередньої сесії читання, якщо вона існує """
        previous_session = SessionReading.objects.filter(user=user, end_reading__isnull=True).first()
        if previous_session:
            time = datetime.time(date.now().hour, date.now().minute, date.now().second)
            previous_session.end_reading = time
            previous_session.save()

        session = SessionReading(user=user, book_id=book_id, start_reading=request.data.get('start_reading'),
                                 date_end_reading=date.today())
        session.save()

        statistics_total_reading_time.delay()

        return Response({'detail': 'Сесію читання розпочато'}, status=status.HTTP_201_CREATED)


class ReadingSessionDetail(APIView):
    queryset = SessionReading.objects.all()
    serializer_class = SessionSerializer

    def get(self, request, sess_id=None):
        session = get_object_or_404(SessionReading, id=sess_id)
        serializer = SessionSerializer(session).data
        return Response(serializer)

    def put(self, request, sess_id=None):
        session = get_object_or_404(SessionReading, id=sess_id)
        session.end_reading = request.data.get('end_reading')
        session.date_end_reading = date.today()
        session.save()
        return Response({'detail': 'Сесія читання завершина'})


class UserAPI(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

