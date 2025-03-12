from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Product
from .forms import OrderForm, OrderItemFormSet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def create_order(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()
            formset.instance = order
            formset.save()
            # After saving the order items, calculate discounts.
            order.calculate_discounts()
            return redirect('order_detail', order_id=order.id)
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, 'create_order.html', {'order_form': order_form, 'formset': formset})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after signup.
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})