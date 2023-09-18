from django.urls import path
from . import views

urlpatterns = [
    path('', views.proxy_request, name='proxy_request_empty'),
    path('add-rule/', views.add_rule, name='add_rule'),
    path('health/', views.health, name='health'),
    path('metrics/', views.prometheus_metrics, name='prometheus_metrics'),
    path('<path:path>/', views.proxy_request, name='proxy_request')
]
