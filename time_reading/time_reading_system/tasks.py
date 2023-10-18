import datetime
from datetime import timedelta
from datetime import datetime as date
from celery import shared_task
from time_reading_system.models import SessionReading, UserProfile


@shared_task()
def statistics_total_reading_time():
    users = UserProfile.objects.all()

    for user in users:
        seven_day = date.today() - timedelta(days=7)
        thirty_day = date.today() - timedelta(days=30)
        session_seven_day = SessionReading.objects.filter(user_id=user.user_id, end_reading__isnull=False,
                                                          date_end_reading__gte=seven_day.date())

        session_thirty_day = SessionReading.objects.filter(user_id=user.user_id,
                                                           end_reading__isnull=False,
                                                           date_end_reading__gte=thirty_day.date())

        user_prof = UserProfile.objects.get(user=user.user)
        user_prof.seven_day_time_reading = counting_full_time_reading(session_seven_day)
        user_prof.thirty_day_time_reading = counting_full_time_reading(session_thirty_day)
        user_prof.save()


""" ОБЧИСЛЕННЯ ЗАГАЛЬНОГО ЧАСУ ЧИТАННЯ """


def counting_full_time_reading(session_day):
    full_time = 0
    for read in session_day:
        start_reading_duration = int(read.start_reading.hour * 3600) + read.start_reading.minute * 60 \
                                 + read.start_reading.second
        end_reading_duration = int(read.end_reading.hour * 3600) + int(read.end_reading.minute * 60) \
                               + read.end_reading.second
        full_time += int(end_reading_duration - start_reading_duration)

    full_reading_time_hours = int(full_time // 3600)
    full_reading_time_minute = int((full_time % 3600) // 60)
    full_reading_time_second = int(full_time % 60)
    full = datetime.time(full_reading_time_hours, full_reading_time_minute, full_reading_time_second)

    return full