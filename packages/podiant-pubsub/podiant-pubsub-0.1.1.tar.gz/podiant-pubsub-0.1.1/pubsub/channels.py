from .models import Message, Tag
from . import subscriptions


def subscription(*channels, tags=(), once=False):
    def wrapper(f):
        for channel in channels:
            subscriptions.register(channel, tags, f, once)

        return f

    return wrapper


def publish(channel, name, *tags, **data):
    message = Message(
        channel=channel,
        name=name
    )

    message.set_data(data)
    message.full_clean()
    message.save()

    for tag in tags:
        t = Tag(message=message, slug=tag)
        t.full_clean()
        t.save()

    message.publish()
