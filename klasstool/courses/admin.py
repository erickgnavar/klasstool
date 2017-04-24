from django.contrib import admin
from django.urls import reverse

from .models import Course, Session


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ('name', 'owner', 'created')
    list_filter = ('owner',)


def generate_qr_codes(modeladmin, request, queryset):
    for session in queryset:
        data = '{scheme}://{host}{url}'.format(
            scheme=request.scheme,
            host=request.get_host(),
            url=reverse('courses:session-public', kwargs={'session_id': session.id})
        )
        session.make_qrcode(data)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'date', 'is_active')
    list_filter = ('course',)
    actions = [
        generate_qr_codes,
    ]
