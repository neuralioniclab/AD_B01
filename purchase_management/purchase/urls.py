from django.urls import path
from purchase import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('suppliers/', views.supplier_list_view, name='supplier_list_view'),
    path('suppliers/create/', views.supplier_create_view, name='supplier_create_view'),
    path('suppliers/<int:pk>/update/', views.supplier_update_view, name='supplier_update_view'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete_view, name='supplier_delete_view'),
    path('purchases/', views.purchase_list_view, name='purchase_list_view'),
    path('purchases/create/', views.purchase_create_view, name='purchase_create_view'),
    path('purchases/<int:pk>/update/', views.purchase_update_view, name='purchase_update_view'),
    path('purchases/<int:pk>/delete/', views.purchase_delete_view, name='purchase_delete_view'),
]
