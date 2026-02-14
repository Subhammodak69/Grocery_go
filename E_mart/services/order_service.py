from E_mart.models import Order,OrderItem,CartItem,Product,Payment
from E_mart.services import cart_service,payment_service,user_service,delivery_service
from decimal import Decimal
from E_mart.constants.default_values import OrderStatus,PaymentStatus,ExchangeOrReturnStatus,DeliveryStatus
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

def get_order_admin_data_by_id(order_id):
    order = Order.objects.filter(id = order_id, is_active = True).first()
    data = {
        'id':order.id,
        'user':order.user,
        'status':order.status,
        'delivery_address':order.delivery_address,
        'total_price':order.total_price,
        'discount':order.discount,
        'delivery_fee':order.delivery_fee,
        'items':get_order_items_data(order),
        'listing_price':order.listing_price,
        'count':len(get_order_items_data(order)),
        'is_active':order.is_active
    }
    return data


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

def get_order_enums_for_delivery():
    enums_data = [
        {
            'value': enum.value,
            'name': enum.name
        }
        for enum in DeliveryStatus
        if enum.name not in [DeliveryStatus.PICKEDUP.name,DeliveryStatus.RETURNED.name]
    ]
    return enums_data

def get_enums_for_pickup():
    enums_data = [
        {
            'value': enum.value,
            'name': enum.name
        }
        for enum in DeliveryStatus
        if enum.name not in [DeliveryStatus.DELIVERED.name]
    ]
    return enums_data


def get_price_summary(order):
    order = Order.objects.get(id=order.id)
    data = {
        'listing_price':order.listing_price,
        'discount':order.discount,
        'delivery_fee':order.delivery_fee,
        'total_price':order.total_price,
    }
    return data


#admin needed

def get_all_orders():
    return Order.objects.all()

def get_order_by_id(order_id):
    return Order.objects.filter(id = order_id).first()

def order_create(user_id, status, total_price, discount, delivery_fee, 
                 listing_price, delivery_address, is_active, items=None):
    user = user_service.get_active_user_obj_by_id(user_id)
    order = Order.objects.create(
        user=user,
        status=int(status),
        total_price=Decimal(total_price),
        discount=Decimal(discount or 0),
        delivery_fee=Decimal(delivery_fee),
        listing_price=Decimal(listing_price),
        delivery_address=delivery_address or None,
        is_active=is_active
    )
    
    if items:
        for item_data in items:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity', 1)
            if product_id:
                try:
                    product = Product.objects.get(id=product_id)
                    
                    # Simple stock check
                    if product.stock >= quantity:
                        item = OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            is_active=True
                        )
                        # Fix: Use quantity and save!
                        product.stock = product.stock - quantity
                        product.save()
                    else:
                        print(f"Not enough stock for product {product_id}")
                        # You can skip this item or raise error
                        
                except Product.DoesNotExist:
                    print(f"Product {product_id} not found")
    
    return order



def order_update(order_id, user_id, status, total_price, discount, 
                 delivery_fee, listing_price, delivery_address, is_active, 
                 current_items, new_items):
    order = Order.objects.get(id=order_id)
    user = user_service.get_active_user_obj_by_id(user_id)
    
    # Store original order items quantities for stock restore
    original_items_quantities = {}
    for item in order.order_items.all():
        original_items_quantities[item.product_id] = item.quantity
    
    # Update order fields
    order.user = user
    order.status = int(status)
    order.total_price = Decimal(total_price)
    order.discount = Decimal(discount or 0)
    order.delivery_fee = Decimal(delivery_fee)
    order.listing_price = Decimal(listing_price)
    order.delivery_address = delivery_address or None
    order.is_active = is_active
    order.save()
    
    # Get current product IDs from frontend
    current_product_ids = [item.get('product_id') for item in current_items if item.get('product_id')]
    
    # Get ALL existing order items from database
    existing_items = order.order_items.all()
    existing_product_ids = [str(item.product_id) for item in existing_items]
    
    # 1. DELETE REMOVED ITEMS (not in current_items) - RESTORE STOCK
    removed_product_ids = set(existing_product_ids) - set(current_product_ids)
    if removed_product_ids:
        for product_id in removed_product_ids:
            product = Product.objects.get(id=product_id)
            old_qty = original_items_quantities.get(int(product_id), 0)
            product.stock = product.stock + old_qty  # ADD BACK STOCK
            product.save()
        
        OrderItem.objects.filter(
            order=order,
            product_id__in=removed_product_ids
        ).delete()
    
    # 2. UPDATE EXISTING ITEMS from current_items - HANDLE STOCK CHANGE
    for item_data in current_items:
        product_id = item_data.get('product_id')
        quantity = item_data.get('quantity', 0)
        
        if product_id and quantity > 0:
            try:
                product = Product.objects.get(id=product_id)
                order_item, created = OrderItem.objects.update_or_create(
                    order=order,
                    product=product,
                    defaults={'quantity': quantity}
                )
                
                # Calculate stock change
                old_qty = original_items_quantities.get(int(product_id), 0)
                stock_change = old_qty - quantity  # Positive = add stock, Negative = reduce stock
                product.stock = product.stock + stock_change
                product.save()
                
            except Product.DoesNotExist:
                print(f"Product {product_id} not found")
    
    # 3. ADD NEW ITEMS from new_items - REDUCE STOCK
    for item_data in new_items:
        product_id = item_data.get('product_id')
        quantity = item_data.get('quantity', 1)
        
        if product_id and quantity > 0:
            try:
                product = Product.objects.get(id=product_id)
                
                # Check if product already exists
                if not OrderItem.objects.filter(order=order, product_id=product_id).exists():
                    # Check stock availability
                    if product.stock >= quantity:
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity
                        )
                        product.stock = product.stock - quantity  # REDUCE STOCK
                        product.save()
                    else:
                        print(f"Not enough stock for product {product_id}")
                        
            except Product.DoesNotExist:
                print(f"Product {product_id} not found")
    
    return order




def toggle_active_order(order_id, is_active):
    order = Order.objects.get(id=order_id)
    order.is_active = bool(is_active)
    order.save()
    return order

def get_order_items(order_id):
    """Get order items for AJAX dropdown population"""
    order = Order.objects.get(id=order_id)
    items = order.order_items.select_related('product').values(
        'id',
        'quantity',
        'product__name'
    )
    
    # Transform data for frontend
    result = []
    for item in items:
        result.append({
            'id': item['id'],
            'product_name': item['product__name'],
            'quantity': item['quantity']
        })
    return result


def get_all_order_status():
    data = [
        {
            'value':status.value,
            'name':status.name
        }
        for status in OrderStatus
    ]
    return data


def get_all_unassigned_orders():
    assigned_orders = delivery_service.get_all_deliveryorpickup_orders()
    assigned_order_ids = list(assigned_orders.values_list('order', flat=True))
    return Order.objects.exclude(id__in=assigned_order_ids).exclude(status = OrderStatus.CANCELLED.value)
