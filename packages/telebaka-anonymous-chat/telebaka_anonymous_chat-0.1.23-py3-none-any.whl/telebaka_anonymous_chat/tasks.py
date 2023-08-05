from celery import shared_task

from telebaka_anonymous_chat.models import User


@shared_task
def reset_media():
    User.objects.update(media_sent=0)
