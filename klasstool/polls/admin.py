from django.contrib import admin

from .models import Poll, Choice, Response


class ChoiceInline(admin.TabularInline):

    model = Choice
    fields = ('value',)


def begin_poll(modeladmin, request, queryset):
    for poll in queryset:
        poll.begin()


def finish_poll(modeladmin, request, queryset):
    for poll in queryset:
        poll.finish()


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):

    list_display = ('title', 'is_active', 'start', 'end', 'session')
    list_filter = ('session',)
    inlines = [ChoiceInline]
    actions = [
        begin_poll,
        finish_poll
    ]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):

    list_display = ('poll', 'choice')
