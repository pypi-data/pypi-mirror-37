from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Notification
import cron


@cron.interval(minutes=5)
def send_notifications():
    notifications_per_user = {}
    for notification in Notification.objects.filter(read=False):
        if notification.user.pk not in notifications_per_user:
            notifications_per_user[notification.user.pk] = []

        notifications_per_user[notification.user.pk].append(notification)

    for user in User.objects.filter(
        pk__in=notifications_per_user.keys()
    ).exclude(
        email=None
    ).exclude(
        email=''
    ):
        messages = []
        subject = ''

        for notification in notifications_per_user[user.pk]:
            messages.append(notification)
            notification.read = True
            notification.save(update_fields=('read',))

            if not subject:
                subject = notification.summary

        if any(messages):
            html = render_to_string(
                'email/notifications/notification.html',
                {
                    'user': user,
                    'messages': messages
                }
            )

            msg = EmailMultiAlternatives(
                subject,
                'You have notifications from Podiant',
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )

            msg.attach_alternative(html, 'text/html')
            msg.send()
