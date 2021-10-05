from . import views
from django.urls import path

urlpatterns = [
    # path('curt', views.curtaclan,name='curta'),
    path('login/', views.log_in,name='login'),
    path('logout/', views.log_out,name='logout'),
    path('register/', views.register,name='register'),
    path('category', views.categoryview,name='category'),
    path('', views.homeview,name='product'),
    path('product/', views.productview,name='product_d'),
    path('product/<str:name>', views.detailview,name='product_details'),
    path('category/<str:name>', views.catprod,name='category_details'),
    path('cart/', views.cartsview,name='cart'),
    path('cart/<str:name>', views.carts_item, name='cart_add'),
    path('cart_edit/<str:name>', views.cartsedit,name='cart_edit'),
    path('cart_delete/<str:name>', views.cartsdelete,name='cart_delete'),
    path('try/<str:name>', views.producttryview,name='tried'),
    path('send/<str:name>', views.send_try,name='send'),
    path('try/', views.triedview, name='try'),
    path('payment', views.payme,name='payment'),
    path('search/', views.search,name='search'),
    path('checkout/', views.checkoutview,name='checkout'),

]
