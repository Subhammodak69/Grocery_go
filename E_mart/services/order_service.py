from E_mart.models import Order,OrderItem,CartItem,Product,Payment
from E_mart.services import cart_service,payment_service,product_service
from decimal import Decimal
from E_mart.constants.default_values import OrderStatus,PaymentStatus
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

def create_order(user, address, final_price, delivery_fee, discount):
    """
    Create an order from the user's cart
    """
    try:
        user_cart = cart_service.get_cart_by_user(user.id)

        cart_items = CartItem.objects.filter(cart=user_cart)

        if not cart_items.exists():
            raise Exception("Cart is empty")

        total = 0
        for item in cart_items:
            # Check stock availability
            if item.product.stock < item.quantity:
                raise Exception(f"Product '{item.product.name}' is out of stock!")
            item_total = item.product.price * item.quantity
            total += item_total

        order = Order.objects.create(
            user=user,
            status=OrderStatus.PENDING.value,
            listing_price=total,
            total_price=final_price,
            delivery_fee=delivery_fee,
            delivery_address=address,
            discount=discount
        )

        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity  # fixed usage here
            )
            product = order_item.product
            product.stock -= cart_item.quantity  # fixed usage here
            product.save()

        # Clear cart items after creating order
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
        if order_item:
            product.stock -= quantity
            product.save()
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
        'orderitems':get_order_items_data(order),
        'is_paid':payment_service.check_order_is_paid(order.id)
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
    orderitems = OrderItem.objects.filter(order = order,is_active = True)
    for item in orderitems:
        product = item.product
        product.stock += item.quantity
        product.save() 

def get_order_by_id(order_id):
    return Order.objects.filter(id = order_id, is_active = True).first()

def get_orderitems_by_order_id(order_id):
    order = get_order_by_id(order_id)
    return  OrderItem.objects.filter(order = order, is_active = True)



def free_garbage_order():
    garbage_orders = Order.objects.filter(
        status__in=[OrderStatus.PENDING.value, OrderStatus.CANCELLED.value],
        is_active=True,
        created_at__lt=timezone.now()-timedelta(hours=24)
    )
    filtered_orders = []
    for order in garbage_orders:
        try:
            payment = Payment.objects.get(order=order)
            if payment.status != PaymentStatus.COMPLETED.value:  
                filtered_orders.append(order)
        except Payment.DoesNotExist:
            filtered_orders.append(order)
    for order in filtered_orders:  # Use the filtered unpaid orders only
        orderitems = OrderItem.objects.filter(order=order, is_active=True).select_related('product')
        for item in orderitems:
            product = item.product
            product.stock += item.quantity
            product.save()
        order.delete()
    return

def get_all_orders(status):
    if status == 'all':
        return Order.objects.all()
    return Order.objects.filter(status = OrderStatus[status].value)

