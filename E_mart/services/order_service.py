from E_mart.models import Order,OrderItem,CartItem,Product
from E_mart.services import cart_service
from decimal import Decimal
from E_mart.constants.default_values import OrderStatus
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

def create_order(user, address,final_price,delivery_fee,discount):
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
            item_total = (item.product.price) * item.quantity
            total += item_total
        
        # Create the order
        order = Order.objects.create(
            user=user,
            status=OrderStatus.PENDING.value,
            listing_price=total,
            total_price = final_price,
            delivery_fee = delivery_fee,
            delivery_address=address,
            discount = discount
        )
        
        # Create OrderItem entries from cart items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
            )
        
        # Clear cart after order creation
        cart_items.delete()
        
        return order
        
    except Exception as e:
        print(f"Error creating order: {str(e)}")
        return None



def sigle_order_create(user, product_id, address, quantity,listing_price,delivery_fee,discount):
    try:
        # Get active product details
        product = Product.objects.get(id=product_id, is_active=True)

        listing_price = product.original_price * int(quantity) 
        total_price = (product.price * int(quantity) )+ Decimal(delivery_fee)
        

        # Create order
        order = Order.objects.create(
            user=user,
            status=OrderStatus.PENDING.value,  # Default status
            listing_price=listing_price,
            total_price = total_price,
            delivery_fee = delivery_fee,
            delivery_address=address,
            discount = discount
        )

        # Create order item
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

        # Return created order (could be used for confirmation, etc.)
        return order

    except Exception as e:
        # Optional: log error, re-raise or handle as needed
        print(f"Error creating order: {e}")
        return None



def get_final_price(total_price):
    discount = (())
    delivery_fee = 0 if total_price >=500 else 20
    return total_price+delivery_fee-discount

def get_all_orders_by_user(user):
    orders = Order.objects.filter(user = user, is_active= True).order_by('-created_at')
    orders_data = [
        {
            'id':order.id,
            'total': order.total_price,
            'updated_at': order.updated_at,
            'status':OrderStatus(order.status).name,
            'status_value':OrderStatus(order.status).value,
            'address':order.delivery_address,
            'orderitems': get_order_items_data(order),
        }
        for order in orders
    ]
    return orders_data

def get_order_items_data(order):
    order_items = OrderItem.objects.filter(order = order, is_active = True)
    order_items_data = [
        {
            'id':item.id,
            'product_id':item.product.id,
            'quantity':item.quantity,
            'image':item.product.image,
            'name':item.product.name,
            'size':item.product.size,
            'price':item.product.price,
            'original_price':item.product.original_price
        }
        for item in order_items
    ]
    return order_items_data

def get_order_full_data(order_id):
    order = Order.objects.filter(id = order_id, is_active=True).first()
    order_data = {
        'id':order.id,
        'address':order.delivery_address,
        'status':order.status,
        'status_value':OrderStatus(order.status).value,
        'orderitems':get_order_items_data(order)
    }
    return order_data

def get_order_price_summary(order_id):
    order = Order.objects.filter(id = order_id, is_active=True).first()
    summary = {
        'listing_price':order.listing_price,
        'total_price': order.total_price,
        'discount':order.discount,
        'delivery_fee':order.delivery_fee
    }
    return summary

def get_delivery_fee(total):
    if total >= Decimal('500'):
        fee = Decimal('0')
    else:
        fee = Decimal('20')
    return fee

def delete_order(order_id, user):
    try:
        order = Order.objects.get(id=order_id, is_active=True)
    except ObjectDoesNotExist:
        raise Exception("Order not found")

    if order.user != user:
        raise PermissionDenied("You do not have permission to cancel this order")

    order.status = OrderStatus.CANCELLED.value
    order.save()
