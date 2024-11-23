# urls.py

from django.urls import path
from tree import views

urlpatterns = [
    path('', views.home, name='home'),  # 기본 URL
    path('register/', views.register, name='register'),
    path('create_tree/<int:user_id>/', views.create_tree, name='create_tree'),
    path('tree_list/', views.tree_list, name='tree_list'),
    path('tree_detail/<int:tree_id>/', views.tree_detail, name='tree_detail'),
    path('write_letter/<int:tree_id>/', views.write_letter, name='write_letter'),
]
