from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
import json
from .models import Cart, Order, OrderItem, Shipment
from products.models import Product
from .forms import OrderForm 




# list of products in cart
class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'cart/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)



# Order Creation View
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_form.html'
    success_url = reverse_lazy('order_success')

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        customer = form.instance.customer
        customer.address = form.cleaned_data['address']  # Save address
        customer.save()
        response = super().form_valid(form)
        items = self.request.POST.getlist('items')
        for item in items:
            item_data = json.loads(item)
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            price = product.display_price
            OrderItem.objects.create(order=self.object, product=product, quantity=quantity, price=price)
        return response


# Order Success View
class OrderSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'order_success.html')


# Order Detail View
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)



# Shipment Detail View
class ShipmentDetailView(LoginRequiredMixin, DetailView):
    model = Shipment
    template_name = 'shipment_detail.html'
    context_object_name = 'shipment'

    def get_queryset(self):
        return Shipment.objects.filter(order__customer=self.request.user.customer)