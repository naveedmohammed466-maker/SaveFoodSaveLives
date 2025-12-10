"""
URL configuration for foodwaste project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
# from FoodO.views import restaurant_dashboard, ngo_dashboard, login_view
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', login_view, name='login_view'),
#     path('ngo_dashboard/',ngo_dashboard, name='ngo_dashboard'),
#     path('restaurant_dashboard/',restaurant_dashboard, name='restaurant_dashboard'),
#     path('ngo_login/', views.ngo_login, name='ngo_login'),
#     path('restaurant_login/', views.restaurant_login, name='restaurant_login'),

# ]

from django.contrib import admin
from django.urls import path # include
from FoodO import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('FoodO.urls')),  # DO NOT CREATE NEW URL FILE

    # Landing / Login page
    path('', views.login_view, name='login'),

    # NGO
    path('ngo_login/', views.ngo_login, name='ngo_login'),
    path('ngo_dashboard/', views.ngo_dashboard, name='ngo_dashboard'),

    # Restaurant
    path('restaurant_login/', views.restaurant_login, name='restaurant_login'),
    path('restaurant_dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('request_pickup/<int:id>/', views.request_pickup, name='request_pickup'),
    path('handle_request/<int:request_id>/', views.handle_request, name='handle_request'),

]








