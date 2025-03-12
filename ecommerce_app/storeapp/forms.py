from django import forms
from .models import Order, OrderItem
from django.forms import inlineformset_factory

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=False)
