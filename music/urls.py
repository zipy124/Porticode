

"""UCL_Music_Player URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
app_name='music'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^location/(?P<location_id>[0-9]+)$', views.location, name='location'),
    url(r'^location/request/(?P<location_id>[0-9]+)$', views.song_request, name='request'),
    url(r'^location/request/list/(?P<location_id>[0-9]+)$', views.song_list, name='list'),
    url(r'^location/request/add/(?P<location_id>[0-9]+)$', views.add_song, name='add'),
    url(r'^location/now_playing/(?P<location_id>[0-9]+)$', views.now_playing, name='now_playing'),
    url(r'^location/setup/(?P<location_id>[0-9]+)$', views.setup, name='setup'),
]
