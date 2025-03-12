## Ecommerce web applications
- http://127.0.0.1:8000/signup/- Create an account.
- http://127.0.0.1:8000/accounts/login/ - User login.
- http://127.0.0.1:8000/products/ -List of products available.
- http://127.0.0.1:8000/orders/<int>/ -  Order details with discount applied.
- http://127.0.0.1:8000/admin/ -Admin panel ,Add Products


## How to run
- Navigate to directory where manage.py file is present.
- RUN: python manage.py runserver
- OPEN: http://127.0.0.1:8000/signup

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


## Recommendation
`
    Improved Recommendation System:
    1. If the user has past orders, count frequency of category.
    2. Identify the most frequently purchased category.
    3. Exclude products the user already purchased in that category.
    4. Recommend the top 5 products (sorted by descending price) from that category.
    5. If no new products are available or if the user has no orders,
       fallback to recommending the top 5 less-expensive products overall.
`

## APIS
- The product_list view displays the list of products and recommendations on a webpage.
- The create_order view allows users to create orders (with discount calculations) via a form, and the order_detail view shows order details.


