from E_mart.models import CartItem

def get_all_cartitems():
    return CartItem.objects.all()

def get_all_cartitems_by_cart(cart):
    return CartItem.objects.filter(cart = cart, is_active=True)

def get_cartitem(cartitem_id):
    return CartItem.objects.get(id = cartitem_id, is_active = True)

def create_cartitem(cart,product,quantity):
    return CartItem.objects.create(
        cart = cart,
        product = product,
        quantity = quantity
    )
    
def update_cartitem(cartitem,quantity):
    return CartItem.objects.update(
        id = cartitem,
        quantity = quantity
    )
    
def deactivate_cartitem(cartitem):
    cartitem.is_active = False
    cartitem.save()
    return cartitem