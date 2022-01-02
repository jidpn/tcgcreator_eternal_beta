"""mysite URL Configuration

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
from django.urls import re_path,path
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout_then_login,LogoutView
import tcgcreator.views
from . import views

urlpatterns = [
    re_path(r'^admin/tcgcreator/field/$',tcgcreator.views.field_list_view,name='field_list_view'),
    re_path(r'^admin/tcgcreator/pac/(?P<pac_id>\d+)/diagram',tcgcreator.views.pac_diagram),
    re_path(r'^admin/tcgcreator/paccost/(?P<pac_id>\d+)/diagram',tcgcreator.views.pac_cost_diagram),
    re_path(r'^admin/tcgcreator/trigger/(?P<trigger_id>\d+)/diagram',tcgcreator.views.trigger_diagram),
    re_path(r'^admin/tcgcreator/trigger/(?P<trigger_id>\d+)/tag_monster',tcgcreator.views.trigger_tag_monster),
    re_path(r'^admin/tcgcreator/trigger/(?P<trigger_id>\d+)/cost_diagram',tcgcreator.views.trigger_cost_diagram),
    re_path(r'^admin/tcgcreator/defaultdeck/$',tcgcreator.views.default_deck,name='defaultdeck2'),
    re_path(r'^admin/tcgcreator/enemydeck/$',tcgcreator.views.enemy_deck,name='enemydeck2'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^tcgcreator/', include('tcgcreator.urls',namespace="tcgcreator")),
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path('', views.index,name='index'),


]
