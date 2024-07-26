from django.urls import path, include
from Goods import views

urlpatterns = [
    path('', views.main, name='index'),
    path('authentication/', include('Goods.authentication.urls')),
    path('back-office/', include('Goods.back-office.urls')),
    path('product_entries/', views.product_enter_list, name='product_enter_list'),
    path('product_entries/create/', views.product_enter_create, name='product_enter_create'),
    path('product_entries/update/<int:pk>/', views.product_enter_update, name='product_enter_update'),
    path('product_entries/delete/<int:pk>/', views.product_enter_delete, name='product_enter_delete'),
]
