from django.db import models
from . import subscriptions
import base64
import pickle


class Message(models.Model):
    channel = models.CharField(max_length=100, db_index=True)
    name = models.SlugField(max_length=100, db_index=True)
    data = models.TextField()
    published = models.DateTimeField(auto_now_add=True)

    def set_data(self, value):
        self.data = base64.b64encode(
            pickle.dumps(value, 0)
        ).decode('utf-8')

    def get_data(self):
        return pickle.loads(base64.b64decode(self.data))

    def publish(self):
        subscriptions.publish(self)

    @property
    def similar_messages(self):
        return type(self).objects.filter(
            channel=self.channel,
            name=self.name,
            tags__slug__in=self.tags.values_list('slug', flat=True),
            data=self.data
        ).exclude(
            pk=self.pk
        )

    def call(self, func):
        return func(
            self.channel,
            self.name,
            *sorted(set(self.tags.values_list('slug', flat=True))),
            **self.get_data()
        )


class Tag(models.Model):
    message = models.ForeignKey(
        Message,
        related_name='tags',
        on_delete=models.CASCADE
    )

    slug = models.SlugField(max_length=100)

    def __str__(self):  # pragma: no cover
        return self.slug

    class Meta:
        unique_together = ('slug', 'message')
