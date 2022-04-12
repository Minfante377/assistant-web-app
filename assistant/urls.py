"""assistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from web import views

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_view, name='register'),
    path('register_user/', views.register_user, name='register_user'),
    path('client/', views.client_view, name='client_view'),
    path('owner/', views.owner_view, name='owner_view'),
    path('owner/calendar/add', views.add_owner_calendar,
         name='add_owner_calendar'),
    path('owner_clients/', views.owner_clients_view,
         name='owner_clients_view'),
    path('owner_clients/delete', views.delete_owner_client,
         name='delete_owner_client'),
    path('owner_clients/add', views.add_owner_client,
         name='add_owner_client'),
    path('available_events/owner/<str:month_filter>&<int:year_filter>',
         views.available_events_view,
         name='available_events_view'),
    path('available_events/owner/',
         views.available_events_view,
         name='available_events_view'),
    path('available_events/add', views.add_event, name='add_event'),
    path('available_events/delete', views.delete_event, name='delete_event'),
    path('admin/', admin.site.urls),
]
