from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^sessions/(?P<session_id>[\w-]+)/polls/$', views.SessionPollListView.as_view()),
    url(r'^sessions/(?P<session_id>[\w-]+)/responses/$', views.PollResponseCreateView.as_view()),
]
