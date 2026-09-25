from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Product Browsing
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    # Reviews
    path('<int:product_id>/add_review/', views.add_review, name='add_review'),

    # Product Detail
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # Cart Management
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),

    # User Authentication
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]