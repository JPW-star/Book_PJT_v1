from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list),
    path('<str:isbn13>/', views.book_detail),
]
