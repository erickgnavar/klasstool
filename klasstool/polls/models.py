from collections import defaultdict

from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from . import notifications


class Poll(TimeStampedModel):

    session = models.ForeignKey('courses.Session')

    title = models.CharField(_('Title'), max_length=255)
    is_active = models.BooleanField(_('Is active?'), default=False)
    start = models.DateTimeField(_('Start'), null=True, blank=True)
    end = models.DateTimeField(_('End'), null=True, blank=True)

    result = JSONField(_('Result'), null=True, blank=True)

    class Meta:
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')
        default_related_name = 'polls'

    def __str__(self):
        return self.title

    def begin(self):
        self.start = timezone.now()
        self.is_active = True
        self.save()
        notifications.poll_started(self)

    def finish(self):
        self.end = timezone.now()
        self.is_active = False
        self._process_responses()
        self.save()
        notifications.poll_finished(self)

    def _process_responses(self):
        res = defaultdict(int)
        for response in self.responses.all().select_related('choice'):
            res[response.choice.value] += 1
        self.result = res


class Choice(TimeStampedModel):

    value = models.CharField(_('Value'), max_length=100)

    poll = models.ForeignKey('Poll')

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')
        default_related_name = 'choices'

    def __str__(self):
        return self.value


class Response(TimeStampedModel):

    poll = models.ForeignKey('Poll')
    choice = models.ForeignKey('Choice')

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')
        default_related_name = 'responses'

    def __str__(self):
        return '{}: {}'.format(self.poll.title, self.choice.value)
