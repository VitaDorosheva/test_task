from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', LoginView.as_view(template_name='referral/login.html'), name='login'),
    url(r'^confirm/$', TemplateView.as_view(template_name='referral/confirm.html')),
    url(r'^profile/$', views.user_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.user_profile, name='view_profile_with_pk'),

]
