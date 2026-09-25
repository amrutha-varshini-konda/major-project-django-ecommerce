from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Review, Order, OrderItem

# 1. Product List & Search View
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True) if hasattr(Product, 'available') else Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


# 2. Product Detail View
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    reviews = product.reviews.all() if hasattr(product, 'reviews') else Review.objects.filter(product=product)
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })


# 3. Add Review View
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, 'Your review has been added successfully!')
    return redirect('store:product_detail', id=product.id, slug=product.slug)


# 4. Cart Views
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            if isinstance(item_data, dict):
                quantity = item_data.get('quantity', 1)
            else:
                quantity = int(item_data)
                
            item_total = float(product.price) * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total,
            })
        except (Product.DoesNotExist, ValueError, TypeError):
            continue

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    str_id = str(product_id)
    
    if str_id in cart:
        if isinstance(cart[str_id], dict):
            cart[str_id]['quantity'] += 1
        else:
            cart[str_id] = {'quantity': int(cart[str_id]) + 1}
    else:
        cart[str_id] = {'quantity': 1}
        
    request.session['cart'] = cart
    messages.success(request, 'Item added to cart.')
    return redirect('store:cart_detail')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    str_id = str(product_id)
    
    if str_id in cart:
        del cart[str_id]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart.')
        
    return redirect('store:cart_detail')


# 5. Checkout View (Saves Order to Database)
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:product_list')

    cart_items = []
    total_price = 0

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else int(item_data)
            item_total = float(product.price) * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'total_price': item_total,
            })
        except Product.DoesNotExist:
            continue

    if request.method == 'POST':
        # Create and save Order in DB
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            email=request.POST.get('email', ''),
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            zip_code=request.POST.get('zip_code', ''),
            total_price=total_price
        )

        # Create OrderItem records for each item
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # Clear cart from session
        request.session['cart'] = {}
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('store:order_list')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


# 6. Order History View
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


# 7. User Authentication Views
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('store:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('store:product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have logged out.')
    return redirect('store:product_list')