from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    address = forms.CharField(max_length=255, required=True)  # Add address field

    class Meta:
        model = Order
        fields = ['total_price', 'address']

    def save(self, commit=True):
        order = super().save(commit=False)
        customer = order.customer
        customer.address = self.cleaned_data['address']
        if commit:
            order.save()
            customer.save()
        return order


