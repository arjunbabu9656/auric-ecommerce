from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.conf import settings

from .models import Product, Category, Cart, CartItem, Order, OrderItem, ContactInquiry
from .forms import RegisterForm, CheckoutForm


# ──────────────────────────── helpers ────────────────────────────

def get_or_create_cart(request):
    """Return the cart for the current user or session."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


# ──────────────────────────── pages ────────────────────────────

def homepage(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/index.html', context)


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    active_category = None

    if category_slug:
        active_category = Category.objects.filter(slug=category_slug).first()
        if active_category:
            products = products.filter(category=active_category)
        else:
            messages.info(request, f'The collection "{category_slug.replace("-", " ").title()}" is coming soon. Showing our full archival range.')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'search_query': search_query,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related': related})


# ──────────────────────────── cart ────────────────────────────

def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_or_create_cart(request)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, f'"{product.name}" added to your cart.')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    cart = get_or_create_cart(request)
    if item.cart == cart:
        item.delete()
        messages.info(request, 'Item removed from cart.')
    return redirect('cart')


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    cart = get_or_create_cart(request)
    qty = int(request.POST.get('quantity', 1))
    if item.cart == cart:
        if qty < 1:
            item.delete()
        else:
            item.quantity = qty
            item.save()
    return redirect('cart')


# ──────────────────────────── checkout ────────────────────────────

def checkout(request):
    cart = get_or_create_cart(request)
    if cart.item_count == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=form.cleaned_data['full_name'],
            email=form.cleaned_data['email'],
            address=form.cleaned_data['address'],
            city=form.cleaned_data['city'],
            postal_code=form.cleaned_data['postal_code'],
            country=form.cleaned_data['country'],
            total_amount=cart.total,
        )
        for ci in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                product_name=ci.product.name,
                quantity=ci.quantity,
                price=ci.product.effective_price,
            )
        cart.items.all().delete()
        return redirect('order_success', pk=order.pk)

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/order_success.html', {'order': order})


# ──────────────────────────── auth ────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Welcome to AURIC!')
        return redirect('homepage')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'homepage'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'orders': orders})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'store/order_history.html', {'orders': orders})


from django.core.mail import send_mail
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # 1. Save to Database (Permanent Backup)
            inquiry = ContactInquiry.objects.create(
                name=name,
                email=email,
                message=message
            )
            
            # 2. Attempt Email Notification
            subject = f"NEW AURIC INQUIRY #{inquiry.id}: {name}"
            full_message = f"Inquiry from: {name} ({email})\n\nMessage:\n{message}\n\n--- View in Admin: http://auric-luxuey-clothes.onrender.com/admin/store/contactinquiry/{inquiry.id}/"
            
            try:
                send_mail(
                    subject,
                    full_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, "Your inquiry has been received! Our team will contact you soon.")
            except Exception as e:
                # Still show success because it SAVED to the DB
                print(f"EMAIL ERROR: {e}")
                messages.success(request, "Message received! (Note: Direct email is delayed, but we have your inquiry in our archive.)")
                
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'store/contact.html', {'form': form})
