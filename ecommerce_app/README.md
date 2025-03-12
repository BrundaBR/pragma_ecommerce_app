## Ecommerce web applications
- http://127.0.0.1:8000/signup/- Create an account.
- http://127.0.0.1:8000/accounts/login/ - User login.
- http://127.0.0.1:8000/products/ -List of products available.
- http://127.0.0.1:8000/orders/<int>/ -  Order details with discount applied.
- http://127.0.0.1:8000/admin/ -Admin panel ,Add Products

## Admin
Credential- username: admin and password:test@1234

## Discounts
- Applies the discount rules:
- a) If total > ₹5000, 10% off on total.
- b) If user has more than 5 past orders, flat ₹500 off.
- c) If more than 3 Electronics items, 5% off on Electronics total.

## Caching  in models.py
- Why Use Caching in models?
- Avoids Recomputing Discount Rule
- Speeds Up Performance
- Improves Scalability

## How to run
- Navigate to directory where manage.py file is present.
- RUN: python manage.py runserver
- OPEN: http://127.0.0.1:8000/signup

