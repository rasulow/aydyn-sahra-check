from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('sargyt/', views.sargyt_check, name='sargyt_check'),
    path('sargyt/download-pdf/', views.download_orders_pdf, name='download_orders_pdf'),
]
