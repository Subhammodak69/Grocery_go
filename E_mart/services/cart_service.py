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


def update_cart_items_quantity(item_id,user,quantity):
    cart_item = CartItem.objects.filter(id = item_id, cart__user = user, is_active = True).first()
    cart_item.quantity = quantity
    cart_item.save()

    cart = cart_item.cart
    summary = get_cart_summary(cart)
    # print(summary)
    return cart_item,summary

def get_cart_summary(cart):
    summary = {
        "total_price": cart.get_total_price(),
        "discount": cart.get_discount_price(),
        "fee": cart.get_fee_price(),
    }
    return summary


def get_cartitem_total_by_item_id(cart_item_id):
    cart_item = CartItem.objects.get(id = cart_item_id, is_active = True)
    total = cart_item.product_details.price * cart_item.quantity
    return total