from E_mart.models import Cart,CartItem

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

def get_all_cart_products_data(user_cart):
    cart_items = CartItem.objects.filter(cart = user_cart, is_active = True)
    data = [
        {
            'id':item.id,
            'product_details':item.product_details,
            'product_id':item.product_details.product.id,
            'product_size':item.product_details.size,
            'product_quantity':item.quantity,
            'product_price':item.product_details.price,
            'product_image':item.product_details.product.image,
        }
        for item in cart_items
    ]
    return data

def remove_item_from_cart(item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id,is_active = True)
        cart_item.delete()                     
        return True
    except CartItem.DoesNotExist:
        return False
    except Exception as e:
        print(f'Error in remove_item_from_cart: {e}')
        return False
    

def get_all_cart_product_items(user_cart):
    return CartItem.objects.filter(cart = user_cart, is_active = True)
