from django.urls import path
from . import views

urlpatterns = [
    path('add-rule/', views.add_rule, name='add_rule'),
    path('<path:path>/', views.proxy_request, name='proxy_request')
]