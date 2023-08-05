from django.db import transaction


__version__ = '0.2.0'


@transaction.atomic()
def notify(user, template, summary=None, kind='info', actions=[], **context):
    from .models import Notification
    from django.template.loader import render_to_string

    text = render_to_string(
        'notifications/%s.html' % template,
        **context
    )

    notification = Notification.objects.create(
        user=user,
        summary=summary or template.replace('_', ' ').capitalize(),
        text=text,
        kind=kind
    )

    for ordering, action in enumerate(actions):
        kind, text, url = action
        notification.actions.create(
            kind=kind,
            text=text,
            url=url,
            ordering=ordering
        )

    notification.send()
