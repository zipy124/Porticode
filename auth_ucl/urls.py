from django.conf.urls import url
from . import views

app_name='auth_ucl'
urlpatterns = [
    url(r'^student/login', views.ucl_login, name='student_login'),
    url(r'^student/callback', views.ucl_callback_url, name='student_callback'),
    url(r'^logout', views.ucl_logout, name='logout'),
    url(r'^error', views.error_page, name='error_page'),
]
