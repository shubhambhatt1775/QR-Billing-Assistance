"""
URL configuration for qr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from qrcus.views import (
    index, register, user_login, logout, view_bill, update_bill_status, 
    admin_dashboard, manage_products, add_product, edit_product, delete_product, 
    payment_status, manage_users, sales_report, preset_billing, cashier_dashboard, 
    create_bill, cashier_preset_items, cashier_payment, cashier_login, cashier_logout, 
    customer_bill, customer_payment, customer_profile, customer_logout, scan_qr, 
    view_current_bill, pay_now, admin_logout, razorpayment, payment_success, view_invoice,
    admin_billing_summary, customer_billing_report
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', user_login, name='login'),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout, name='logout'),
    path('bill/', view_bill, name='bill'),
    path('process-payment/', update_bill_status, name='process_payment'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('manage_products/', manage_products, name='manage_products'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:id>/', edit_product, name='edit_product'),
    path('delete_product/<int:id>/', delete_product, name='delete_product'),
    path('preset_billing/', preset_billing, name='preset_billing'),
    path('manage_users/', manage_users, name='manage_users'),
    path('payment_status/', payment_status, name='payment_status'),
    path('sales_report/', sales_report, name='sales_report'),
    path('admin_billing_summary/', admin_billing_summary, name='admin_billing_summary'),
    path('customer_report/<int:customer_id>/', customer_billing_report, name='customer_billing_report'),
    path('admin-logout/', admin_logout, name='admin_logout'),

    path('cashier_login/', cashier_login, name='cashier_login'),
    path('cashier_dashboard/', cashier_dashboard, name='cashier_dashboard'),
    path('cashier_logout/', cashier_logout, name='cashier_logout'),
    path('create_bill/', create_bill, name='create_bill'),
    path('preset_items/', cashier_preset_items, name='cashier_preset_items'),
    path('payment/', cashier_payment, name='cashier_payment'),

    # customer Dashboard card actions
    path('customer_bill/', customer_bill, name='customer_bill'),
    path('customer_payment/', customer_payment, name='customer_payment'),
    path('customer_profile/', customer_profile, name='customer_profile'),
    path('customer_logout/', customer_logout, name='customer_logout'),
    
    # Dashboard card actions
    path('scan_qr/', scan_qr, name='scan_qr'),
    path('view_current-bill/', view_current_bill, name='view_current_bill'),
    path('pay_now/', pay_now, name='pay_now'),
    path('pay_now/<int:bill_id>/', pay_now, name='pay_now_with_id'),

    path('razorpayment/', razorpayment, name='razorpayment'),
    path('payment_success/', payment_success, name='payment_success'),
    path('view_invoice/<int:bill_id>/', view_invoice, name='view_invoice')
]
