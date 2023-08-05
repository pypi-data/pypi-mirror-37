from .exceptions import AlreadyRegisteredError
import logging
import re


class SubscriptionList(object):
    def __init__(self):
        self._subs = []
        self._logger = logging.getLogger('podiant.pubsub')

    def register(self, channel, tags, func, once=False):
        key = '^' + channel.replace(
            '.', '\\.'
        ).replace('*', '([a-z0-9]+)') + '$'
        ex = re.compile(key)

        for (e, t, f, o) in self._subs:
            if f == func and e == ex:
                raise AlreadyRegisteredError(
                    '%s is already registered.' % (func.__name__)
                )

        self._subs.append(
            (
                ex,
                tags,
                func,
                once
            )
        )

    def publish(self, message):
        self._logger.debug(
            'Publishing on channel \'%s\'' % message.channel
        )

        for ex, listening_tags, func, once in self._subs:
            if ex.match(message.channel) is None:
                continue

            if any(listening_tags):
                if not message.tags.filter(
                    slug__in=listening_tags
                ).exists():
                    continue

            if once and message.similar_messages.exists():
                self._logger.debug(
                    (
                        'Not sending to %s as this message has already been '
                        'broadcast'
                    ) % func.__name__
                )

                continue

            self._logger.debug(
                'Sending to %s' % func.__name__
            )

            try:
                message.call(func)
            except Exception:
                self._logger.error(
                    'Error running action hook',
                    extra={
                        'channel_name': message.channel,
                        'msg_name': message.name,
                        'msg_data': message.get_data(),
                        'msg_func': func.__name__
                    },
                    exc_info=True
                )
