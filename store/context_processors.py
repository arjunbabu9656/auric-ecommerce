from .models import Cart


def cart_count(request):
    """Inject cart item count into all templates."""
    count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()

    if cart:
        count = cart.item_count

    return {'cart_count': count}
