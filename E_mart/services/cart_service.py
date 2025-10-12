from E_mart.models import Cart

def get_all_carts():
    return Cart.objects.all()

def get_cart_by_user(user):
    is_cart = Cart.objects.filter(user = user, is_active = True).exists()
    if not is_cart:
        return Cart.objects.create(user = user)
    return Cart.objects.filter(user = user, is_active = True).first()

def create_cart(user):
    return Cart.objects.create(
        user = user
    )
    
def deactivate_cart(cart):
    cart.is_active = False
    cart.save()
    return cart