from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^sessions/(?P<session_id>[\w-]+)/$', views.SessionPublicView.as_view(), name='session-public')
]
