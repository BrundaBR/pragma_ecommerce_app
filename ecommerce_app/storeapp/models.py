from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from django.core.cache import cache


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount_breakdown = models.TextField(blank=True, null=True)  # e.g., stored as JSON or text


    def get_discount_rules():
        """
        Retrieve discount rules from the cache.
        If not present, compute or load them and store in cache.
        """
        rules = cache.get('discount_rules')
        if not rules:
            rules = {
                'percentage_discount_threshold': Decimal("5000"),
                'percentage_discount_rate': Decimal("0.10"),
                'flat_discount_order_threshold': 5, 
                'flat_discount_amount': Decimal("500"),
                'category': "electronics",
                'category_discount_quantity_threshold': 3,
                'category_discount_rate': Decimal("0.05"),
            }
            # Cache the rules for 1 hour (3600 seconds)
            cache.set('discount_rules', rules, timeout=3600)
        return rules

    def calculate_discounts(self):
        """
        Applies the discount rules:
          a) If total > ₹5000, 10% off on total.
          b) If user has more than 5 past orders, flat ₹500 off.
          c) If more than 3 Electronics items, 5% off on Electronics total.
        """
        items = self.order_items.all()
        total = sum(item.product.price * item.quantity for item in items)
        breakdown = {}
        discount_total = 0

        # Rule a: Percentage discount on entire order if total exceeds ₹5000.
        perc_discount = Decimal("0.0")
        if total >= Decimal("5000"):
            perc_discount = total * Decimal("0.10")  # Use Decimal for the percentage multiplier
            breakdown['percentage_discount'] = f"10% off: ₹{perc_discount:.2f}"
            discount_total += perc_discount

        # Rule b: Flat discount if user has placed more than 5 orders previously.
        flat_discount = 0
        past_order_count = self.user.orders.exclude(id=self.id).count()
        if past_order_count > 5:
            flat_discount = 500
            breakdown['flat_discount'] = "Flat ₹500 off"
            discount_total += flat_discount

        # Rule c: Category-based discount for Electronics
        electronics_total = sum(item.product.price * item.quantity for item in items 
                                if item.product.category.lower() == "electronics")
        electronics_quantity = sum(item.quantity for item in items 
                                   if item.product.category.lower() == "electronics")
        cat_discount = 0
        if electronics_quantity > 3:
            cat_discount = electronics_total * 0.05
            breakdown['electronics_discount'] = f"5% off on electronics: ₹{cat_discount:.2f}"
            discount_total += cat_discount

        self.total_amount = total
        self.discount_total = discount_total
        self.final_amount = total - discount_total
        self.discount_breakdown = str(breakdown)
        self.save()

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
