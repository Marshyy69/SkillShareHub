from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('gig/create/', views.create_gig, name='create_gig'),
    path('gig/<int:gig_id>/', views.gig_detail, name='gig_detail'),
    path('gig/<int:gig_id>/edit/', views.update_gig, name='update_gig'),
    path('gig/<int:gig_id>/delete/', views.delete_gig, name='delete_gig'),
    path('gig/<int:gig_id>/order/', views.order_gig, name='order_gig'),
    path('orders/', views.my_orders, name='my_orders'),
    path('seller-orders/', views.seller_orders, name='seller_orders'),
    path('order/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('order/<int:order_id>/submit/', views.submit_work, name='submit_work'),
    path('order/<int:order_id>/complete/', views.complete_order, name='complete_order'),
]
