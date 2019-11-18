"""whatsupdoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from . import views
from .models import Tickets

admin.site.register(Tickets)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),
    path('newticketform/', views.new_ticket_form_view,
         name='newticketform'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/<int:id>/', views.edit_ticket_view, name='edit'),
    path('dev/<int:id>/', views.dev_person_view, name='dev'),
    path('ticket/<int:id>/', views.ticket_detail_view, name='ticket')]
