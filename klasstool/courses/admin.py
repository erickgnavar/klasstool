from django.contrib import admin

from .models import Course, Session


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ('name', 'owner', 'created')
    list_filter = ('owner',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

    list_display = ('name', 'date', 'is_active', 'uuid')
    list_filter = ('course',)
