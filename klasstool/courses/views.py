from django.views import generic as gen

from .models import Session


class SessionPublicView(gen.DetailView):

    template_name = 'courses/session_public.html'
    model = Session
    context_object_name = 'session'
    pk_url_kwarg = 'session_id'
