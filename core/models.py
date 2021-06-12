
from django.contrib.auth.models import User
from django.db.models import (Model, TextField, DateTimeField, ForeignKey, IntegerField,
                              CASCADE)

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from torchmoji.classifier.classifier import Classifier

auto_emoji = Classifier()

class MessageModel(Model):
    """
    This class represents a chatcannot import name 'Classifier' from 'torchmoji.classifier'  message. It has a owner (user), timestamp and
    the message body.

    """
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = ForeignKey(User, on_delete=CASCADE, verbose_name='recipient',
                           related_name='to_user', db_index=True)
    sid = IntegerField('sid')
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    body = TextField('body')

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.id))
        print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()   # Trimming whitespaces from the body
        #remocve auto-prediction
        #self.body = auto_emoji.add_emoji(self.body)
        super().save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = 'core'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)


class ScenarioModel(Model):
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='user1',
                      related_name='user1', db_index=True)
    recipient = ForeignKey(User, on_delete=CASCADE, verbose_name='user2',
                           related_name='user2', db_index=True)
    sid = IntegerField('sid')
