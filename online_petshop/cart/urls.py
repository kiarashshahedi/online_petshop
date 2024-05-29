# urls.py
from django.urls import path
from .views import CartListView, OrderCreateView, OrderSuccessView, OrderDetailView, ShipmentDetailView

urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/success/', OrderSuccessView.as_view(), name='order_success'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('shipment/<int:pk>/', ShipmentDetailView.as_view(), name='shipment_detail'),
]
