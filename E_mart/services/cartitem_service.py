from E_mart.models import CartItem
from E_mart.services import product_service

def get_all_cartitems():
    return CartItem.objects.all()

def get_all_cartitems_by_cart(cart):
    items = CartItem.objects.filter(cart = cart, is_active=True)
    items_data = [
        {
            'id':item.id,
            'product_id':item.product.id,
            'product_name':item.product.name,
            'product_description':item.product.description,
            'product_size':item.product.size,
            'product_price':item.product.price,
            'stock':item.product.stock,
            'product_image':item.product.image,
            'quantity':item.quantity,
            'item_total':item.quantity * item.product.price
        }
        for item in items
    ]
    return items_data

def get_cartitem(cartitem_id):
    return CartItem.objects.get(id = cartitem_id, is_active = True)

def create_cartitem(cart,product_id,quantity):
    product_obj = product_service.get_product_by_id(product_id)
    return CartItem.objects.create(
        cart = cart,
        product = product_obj,
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