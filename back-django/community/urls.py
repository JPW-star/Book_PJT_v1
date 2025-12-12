from django.urls import path
from . import views

urlpatterns = [
    path('threads/', views.thread_list_create),
    path('threads/<int:thread_pk>/', views.thread_detail),
    path('threads/<int:thread_pk>/comments/', views.comment_create),
    path('comments/<int:comment_pk>/', views.comment_delete),
    path('threads/<int:thread_pk>/likes/', views.thread_likes),
]
