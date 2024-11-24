from django.urls import path
from tree import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),  # 로그아웃 URL
    path('register/', views.register, name='register'),
    path('create_tree/<int:user_id>/', views.create_tree, name='create_tree'),
    path('tree_list/', views.tree_list, name='tree_list'),
    path('tree_detail/<int:tree_id>/', views.tree_detail, name='tree_detail'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
