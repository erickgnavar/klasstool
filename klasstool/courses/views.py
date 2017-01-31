from django.shortcuts import get_object_or_404
from django.views import generic as gen

from .models import Session


class SessionPublicView(gen.DetailView):

    template_name = 'courses/session_public.html'
    model = Session
    context_object_name = 'session'

    def get_object(self, queryset=None):
        return get_object_or_404(Session, uuid=self.kwargs.get('session_uuid'))
