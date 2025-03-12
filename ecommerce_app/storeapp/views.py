from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Product
from .forms import OrderForm, OrderItemFormSet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse


@login_required
def product_list(request):
    # Retrieve all products to display
    products = Product.objects.all()
    
    # Recommendation logic: If the user has orders, recommend products from their most purchased category;
    # otherwise, return top 5 expensive products.
    user = request.user
    orders = Order.objects.filter(user=user)
    if orders.exists():
        category_counts = {}
        purchased_product_ids = set()

        for order in orders:
            for item in order.order_items.all():
                cat = item.product.category.lower()
                category_counts[cat] = category_counts.get(cat, 0) + item.quantity
                purchased_product_ids.add(item.product.id)

        if category_counts:
            recommended_category = max(category_counts, key=category_counts.get)
            recommended_products = Product.objects.filter(category__iexact=recommended_category)\
                                                  .exclude(id__in=purchased_product_ids)\
                                                  .order_by('-price')
        if not recommended_products.exists():
            recommended_products = Product.objects.all().order_by('-price')[:3]
        
    else:
        #If user has not odered so far, return less-expensive products 
        recommended_products = Product.objects.all().order_by('price')[:5]

    context = {
        'products': products,
        'recommended_products': recommended_products,
    }
    return render(request, 'product_list.html', context)

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

