from django.urls import path
from . import views

app_name = 'asthma'

urlpatterns = [
    path('', views.asthma_page, name='asthma_page'),
#    path('updateRecord/', views.update_record, name='update_record'),
#    path('getHistory/', views.get_patient_history, name='get_patient_history'),
]
