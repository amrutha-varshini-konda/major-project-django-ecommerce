import os
import django
import requests
from django.core.files.base import ContentFile
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from store.models import Product
# Sample unsplash placeholder image URLs by keyword
IMAGES = {
    'headphone': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500',
    'watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500',
    'keyboard': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500',
    'mouse': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500',
    'jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500',
    'shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500',
    't-shirt': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500',
    'bottle': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500',
    'lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500',
}
def attach_images():
    print("Downloading and attaching sample images...")
    products = Product.objects.all()
    for product in products:
        name_lower = product.name.lower()
        image_url = None
        for key, url in IMAGES.items():
            if key in name_lower:
                image_url = url
                break
        if not image_url:
            image_url = 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500'
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                file_name = f"{product.slug}.jpg"
                product.image.save(file_name, ContentFile(response.content), save=True)
                print(f"? Added image to: {product.name}")
        except Exception as e:
            print(f"? Failed to download image for {product.name}: {e}")
    print("\n?? All products updated with images!")
if __name__ == '__main__':
    attach_images()
