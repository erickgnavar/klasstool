from django.dispatch import receiver
from django.db.models.signals import post_save

from klasstool.polls import notifications


@receiver(post_save, sender='polls.Poll')
def post_save_poll(sender, **kwargs):
    if not kwargs.get('created'):
        notifications.poll_updated(kwargs.get('instance'))


@receiver(post_save, sender='polls.Choice')
def post_save_choice(sender, **kwargs):
    # TODO: remove this after create a UI for admin
    notifications.poll_updated(kwargs.get('instance').poll)
