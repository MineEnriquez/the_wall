from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^wall$', views.wall),
    url(r'^wall_render$', views.wall_render),   #----- INCLUDE
    url(r'^validate_login$', views.validate_login),
    url(r'^logout$', views.logout),
    url(r'^post_message$', views.post_message),
    url(r'^post_comment$', views.post_comment),
]
