from django.urls import path
from . import views 
# from .models import Payment

urlpatterns = [
    path('place_order/', views.place_order, name ='place_order'),
    path('payments/',views.payments,name='payments'),
    ]