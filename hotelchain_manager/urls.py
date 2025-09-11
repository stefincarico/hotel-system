"""
URL configuration for hotelchain_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from gestione_hotel.views import homepage_view 
from gestione_hotel.views import homepage_view, hotel_detail_view,hotel_create_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name='homepage'),
    path('hotel/<int:pk>/', hotel_detail_view, name='hotel_detail'),
    path('hotel/nuovo/', hotel_create_view, name='hotel_create'),
]
