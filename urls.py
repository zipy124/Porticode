from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^auth/', include('auth.urls'),namespace="auth"),
    url(r'music/',include('music.urls'),namespace="music"),
    url(r'^admin/', admin.site.urls),
]
