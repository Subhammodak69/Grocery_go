from E_mart.models import CartItem
from E_mart.services import product_details_service

def get_all_cartitems():
    return CartItem.objects.all()

def get_all_cartitems_by_cart(cart):
    items = CartItem.objects.filter(cart = cart, is_active=True)
    items_data = [
        {
            'id':item.id,
            'product_id':item.product_details.product.id,
            'product_name':item.product_details.product.name,
            'product_description':item.product_details.product.description,
            'product_size':item.product_details.size,
            'product_price':item.product_details.price,
            'stock':item.product_details.stock,
            'product_image':item.product_details.product.image,
            'quantity':item.quantity,
        }
        for item in items
    ]
    return items_data

def get_cartitem(cartitem_id):
    return CartItem.objects.get(id = cartitem_id, is_active = True)

def create_cartitem(cart,product_details_id,quantity):
    product_details_obj = product_details_service.get_product_details_by_id(product_details_id)
    return CartItem.objects.create(
        cart = cart,
        product_details = product_details_obj,
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