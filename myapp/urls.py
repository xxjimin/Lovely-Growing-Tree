from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_tree/', views.user_tree, name='user_tree'),
    path('add_letter/<int:tree_id>/', views.add_letter, name='add_letter'),
]
