from django.db import models
from pubsub import channels
from .querysets import NotificationQuerySet


class Notification(models.Model):
    user = models.ForeignKey(
        'auth.User',
        related_name='notifications',
        on_delete=models.CASCADE
    )

    text = models.TextField()
    summary = models.CharField(max_length=255)
    kind = models.CharField(max_length=20, db_index=True)
    sent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False, db_index=True)

    objects = NotificationQuerySet.as_manager()

    def __str__(self):  # pragma: no cover
        return self.summary

    def send(self):
        channels.publish(
            'user.notifications',
            'create',
            self.kind,
            username=self.user.username,
            notification={
                'text': '' + self.text,
                'summary': '' + self.summary,
                'kind': self.kind
            },
            badge=self.user.notifications.unread().count()
        )

        channels.publish(
            'user.messages',
            'create',
            self.kind,
            username=self.user.username,
            kind=self.kind,
            text=self.summary
        )

    class Meta:
        ordering = ('-sent',)
        get_latest_by = 'sent'


class Action(models.Model):
    notification = models.ForeignKey(
        Notification,
        related_name='actions',
        on_delete=models.CASCADE
    )

    kind = models.CharField(max_length=20, db_index=True)
    text = models.CharField(max_length=100)
    url = models.URLField(max_length=512)
    ordering = models.PositiveIntegerField(default=0)

    def __str__(self):  # pragma: no cover
        return self.text

    class Meta:
        ordering = ('ordering',)
        unique_together = ('url', 'notification')
