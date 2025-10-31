from E_mart.models import Order,OrderItem,CartItem,ProductDetails
from E_mart.services import cart_service

def create_order(user, address):
    """
    Create an order from the user's cart
    """
    try:
        user_cart = cart_service.get_cart_by_user(user.id)
        
        # Get CartItem objects directly - DON'T convert to dict
        cart_items = CartItem.objects.filter(cart=user_cart)
        
        if not cart_items.exists():
            raise Exception("Cart is empty")
        
        # Calculate total price correctly
        total = 0
        for item in cart_items:
            item_total = (item.product_details.price) * item.quantity
            total += item_total
        
        # Create the order
        order = Order.objects.create(
            user=user,
            status='pending',
            total_price=total,
            delivery_address=address
        )
        
        # Create OrderItem entries from cart items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_details=cart_item.product_details,
            )
        
        # Clear cart after order creation
        cart_items.delete()
        
        return order
        
    except Exception as e:
        print(f"Error creating order: {str(e)}")
        return None



def sigle_order_create(user, product_details_id, address, quantity):
    try:
        # Get active product details
        product_details = ProductDetails.objects.get(id=product_details_id, is_active=True)

        # Calculate total price (consider discount/quantity if required)
        total_price = product_details.price * int(quantity)  # Basic total calculation
        final_price = get_final_price(total_price, quantity)

        # Create order
        order = Order.objects.create(
            user=user,
            status='pending',  # Default status
            total_price=final_price,
            delivery_address=address
        )

        # Create order item
        order_item = OrderItem.objects.create(
            order=order,
            product_details=product_details,
            quantity=quantity
        )

        # Return created order (could be used for confirmation, etc.)
        return order

    except Exception as e:
        # Optional: log error, re-raise or handle as needed
        print(f"Error creating order: {e}")
        return None


def get_discount_for_sigle_item(total):
        if total >= 2000:
            return total * 0.30
        elif total >= 1000:
            return total * 0.20
        elif total >= 500:
            return total * 0.10
        return 0

def get_final_price(total_price, quantity):
    discount = get_discount_for_sigle_item(total_price)
    delivery_fee = 0 if total_price >=500 else 20
    return total_price+delivery_fee-discount

def get_all_orders_by_user(user):
    orders = Order.objects.filter(user = user, is_active= True).order_by('-created_at')
    orders_data = [
        {
            'id':order.id,
            'total': order.total_price,
            'created_at': order.created_at,
            'status':order.status,
            'address':order.delivery_address,
            'orderitems': get_order_items_data(order)
        }
        for order in orders
    ]
    return orders_data

def get_order_items_data(order):
    order_items = OrderItem.objects.filter(order = order, is_active = True)
    order_items_data = [
        {
            'id':item.id,
            'quantity':item.quantity,
            'product_details':item.product_details
        }
        for item in order_items
    ]
    return order_items_data