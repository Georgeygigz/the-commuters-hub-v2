"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from .views import (ScheduleRouteApiView, RouteJoinAPiView,
                    RouteRetrieveApiView,RoutesRetrieveApiView)

urlpatterns = [
    path('schedule', ScheduleRouteApiView.as_view(), name='schedule-route'),
    path('join', RouteJoinAPiView.as_view(), name='join-route'),
    path('retrieve', RoutesRetrieveApiView.as_view(
         {'get': 'search'}), name='retrieve-route'),
    path('<str:route_id>', RouteRetrieveApiView.as_view(), name='route'),
]
