from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'pos'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
    
    # Point of Sale
    path('pos/', views.point_of_sale, name='point_of_sale'),
    path('pos/process-sale/', views.process_sale, name='process_sale'),
    
    # Sales
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    
    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    
    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    
    # Purchases
    path('purchases/', views.purchase_list, name='purchase_list'),
    
    # Users
    path('users/', views.user_list, name='user_list'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
] 