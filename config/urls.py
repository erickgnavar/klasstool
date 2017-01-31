from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('klasstool.website.urls', namespace='website')),
    url(r'^', include('klasstool.courses.urls', namespace='courses')),
]
