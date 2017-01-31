from io import BytesIO
from uuid import uuid4

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from qrcode import QRCode


class Course(TimeStampedModel):

    name = models.CharField(_('Name'), max_length=50)
    description = models.CharField(_('Description'), max_length=255)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        default_related_name = 'courses'

    def __str__(self):
        return self.name


class Session(TimeStampedModel):

    name = models.CharField(_('Name'), max_length=50)
    date = models.DateField(_('Date'))
    course = models.ForeignKey('Course')
    uuid = models.UUIDField(default=uuid4, editable=False)
    qrcode = models.ImageField(upload_to='sessions/qrcodes/%Y/%m/%d/', null=True, blank=True)
    is_active = models.BooleanField(_('Is active?'), default=False)

    class Meta:
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')
        default_related_name = 'sessions'

    def __str__(self):
        return self.name

    def enable(self):
        self.is_active = True
        self.save()

    def disable(self):
        self.is_active = False
        self.save()

    def make_qrcode(self, data):
        qrcode = QRCode(version=1, box_size=10, border=4)
        qrcode.add_data(data)
        qrcode.make(fit=True)
        im = qrcode.make_image()
        buffer = BytesIO()
        im.save(buffer, im.kind)
        tmp = InMemoryUploadedFile(buffer, None, str(self.uuid), 'image/png', buffer.tell(), None)
        self.qrcode = tmp
        self.save()
