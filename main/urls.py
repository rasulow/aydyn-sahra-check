from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('sargyt/', views.sargyt_check, name='sargyt_check'),
    path('api/add-client/', views.add_client, name='add_client'),
    path('api/update-wallet/', views.update_wallet, name='update_wallet'),
    path('api/save-excel/', views.save_excel_to_check, name='save_excel_to_check'),
]
