import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from store.models import Category, Product, Review
User = get_user_model()
def run():
    print("Seeding database...")
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    user.set_password('password123')
    user.save()
    data = {
        'Electronics': [
            {'name': 'Wireless Noise-Canceling Headphones', 'price': 149.99, 'description': 'High quality over-ear headphones with active noise cancellation.'},
            {'name': 'Smart Watch Series 5', 'price': 199.99, 'description': 'Fitness tracker with heart rate monitor, GPS, and OLED display.'},
            {'name': 'Mechanical Gaming Keyboard', 'price': 89.99, 'description': 'RGB backlit mechanical keyboard with blue tactile switches.'},
            {'name': 'Ergonomic Wireless Mouse', 'price': 29.99, 'description': 'Precision optical mouse with comfortable grip and rechargeable battery.'},
        ],
        'Apparel': [
            {'name': 'Classic Denim Jacket', 'price': 59.99, 'description': '100% cotton casual denim jacket for everyday wear.'},
            {'name': 'Performance Running Shoes', 'price': 79.99, 'description': 'Lightweight breathable sneakers designed for long-distance running.'},
            {'name': 'Cotton Crewneck T-Shirt', 'price': 19.99, 'description': 'Soft slim-fit t-shirt available in premium combed cotton.'},
        ],
        'Home & Living': [
            {'name': 'Stainless Steel Insulated Bottle', 'price': 24.99, 'description': 'Keeps drinks cold for 24 hours or hot for 12 hours.'},
            {'name': 'Desk LED Lamp', 'price': 34.99, 'description': 'Dimmable desk lamp with wireless phone charging pad.'},
        ]
    }
    for cat_name, products in data.items():
        category, _ = Category.objects.get_or_create(
            name=cat_name,
            defaults={'slug': slugify(cat_name)}
        )
        for item in products:
            product, created = Product.objects.get_or_create(
                name=item['name'],
                defaults={
                    'category': category,
                    'slug': slugify(item['name']),
                    'price': item['price'],
                    'description': item['description'],
                    'is_available': True
                }
            )
            if created:
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=5,
                    comment='Absolutely love this item! Exceeded my expectations.'
                )
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=4,
                    comment='Great quality for the price. Would buy again.'
                )
    print("Success! Added sample categories, products, and reviews.")
if __name__ == '__main__':
    run()
