from django.urls import path
from .views import (
    doctor_list_create, doctor_detail, 
    review_list_create, review_detail
)

app_name = 'api'

urlpatterns = [
    # Доктора
    path('doctors/', doctor_list_create, name='doctor-list'),
    path('doctors/<int:pk>/', doctor_detail, name='doctor-detail'),
    
    # Отзывы
    path('reviews/', review_list_create, name='review-list'),
    path('reviews/<int:pk>/', review_detail, name='review-detail'),
]