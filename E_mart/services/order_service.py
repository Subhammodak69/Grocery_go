from E_mart.models import Order,OrderItem,CartItem
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
