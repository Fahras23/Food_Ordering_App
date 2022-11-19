from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('restaurant/<str:pk>',views.restaurant,name='restaurant'),
    path('orders/',views.orders,name='orders'),
    path('account/',views.account,name='account'),
    path('order/<str:pk>',views.order,name='order'),
    
]