from django.urls import path
from .views import index,register,user_login,logout,view_bill

urlpatterns = [
    
    path('',index,name='index'),
    path('register/',register,name='register'),
    path('login/',user_login,name='login'),
    path('logout/',logout,name='logout'),
    path('bill/', view_bill, name='bill')
    
]
