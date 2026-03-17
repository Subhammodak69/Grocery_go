from E_mart.models import ExchangeOrReturn,Order,OrderItem,ExOrReItems,User
from django.utils import timezone
from E_mart.constants.default_values import ExchangeOrReturnStatus,ExOrRePurpose
from django.db import transaction
from django.core.exceptions import ValidationError


@transaction.atomic  # Decorator: entire function is atomic
def create_exchange_or_return(*, order_id, order_item_ids, user, purpose, reason):
    """
    Create exchange/return request with multiple items atomically.
    Returns created ExchangeOrReturn or raises ValidationError.
    """
    # Validate order exists and belongs to user
    order = Order.objects.select_for_update().get(id=order_id)  # Lock for concurrency
    if order.user != user:
        raise ValidationError("Order does not belong to user")
    
    # Filter active order items from this order only
    order_items = OrderItem.objects.filter(
        id__in=order_item_ids,
        is_active=True,
        order=order  # Ensure items from this order
    )
    if order_items.count() != len(order_item_ids):
        raise ValidationError("Some order items not found or inactive")
    
    # Calculate total from items
    total = sum(item.product.price for item in order_items)  # Assumes OrderItem has total_price
    
    # Create main request
    exchange_or_return = ExchangeOrReturn.objects.create(
        order=order,
        user=user,
        reason=reason,
        total=total,
        purpose=int(purpose)
    )
    
    # Bulk create items for efficiency
    items_to_create = [
        ExOrReItems(
            exchange_or_return=exchange_or_return,
            order_item=item,
            quantity=item.quantity
        )
        for item in order_items
    ]
    ExOrReItems.objects.bulk_create(items_to_create)
    
    return exchange_or_return 

def get_exchnage_or_return_items(exchange_or_return):
    return ExOrReItems.objects.filter(exchange_or_return = exchange_or_return,is_active = True)

def get_all_exchanges_or_returns_by_user(user):
    exchanges_or_returns = ExchangeOrReturn.objects.filter(user=user).order_by('-request_date')
    exchanges_or_returns_data = [
        {
            'id': item.id,
            'total': item.total,
            'status': ExchangeOrReturnStatus(item.status).name,
            'status_value': ExchangeOrReturnStatus(item.status).value,
            'address': item.order.delivery_address,
            'purpose':ExOrRePurpose(item.purpose).name,
            'request_date': item.request_date,
            'items': get_exchnage_or_return_items(item)
        }
        for item in exchanges_or_returns
    ]
    return exchanges_or_returns_data

def get_exchange_return_by_id_for_user(pickup_id, user):
    return (
        ExchangeOrReturn.objects
        .select_related('order', 'user')
        .filter(id=pickup_id, user=user)
        .first()
    )





def get_all_exchanges():
    return ExchangeOrReturn.objects.select_related('order', 'user').prefetch_related('exchange_return_items__order_item__product').all()

def get_exchange_by_id(exchange_id):
    return ExchangeOrReturn.objects.select_related('order', 'user').prefetch_related('exchange_return_items__order_item__product').get(id=exchange_id)

@transaction.atomic
def exchange_create(order_id, order_item_ids, user_id, reason, status, purpose, is_active):
    """
    Create an exchange/return request with multiple items
    order_item_ids: list of order item IDs or comma-separated string
    """
    from E_mart.models import Order, User
    
    order = Order.objects.get(id=order_id)
    user = User.objects.get(id=user_id)
    
    # Parse order item IDs
    if isinstance(order_item_ids, str):
        item_ids = [int(id.strip()) for id in order_item_ids.split(',') if id.strip()]
    else:
        item_ids = order_item_ids or []
    
    # Calculate total from order items
    total = 0
    order_items = []
    for item_id in item_ids:
        try:
            order_item = OrderItem.objects.select_related('product').get(id=item_id, order=order)
            order_items.append(order_item)
            total += order_item.product.price * order_item.quantity
        except OrderItem.DoesNotExist:
            continue
    
    # Create exchange request
    exchange = ExchangeOrReturn.objects.create(
        order=order,
        user=user,
        reason=reason,
        total=total,
        status=int(status),
        purpose=int(purpose),
        is_active=is_active
    )
    
    # Create exchange items
    for order_item in order_items:
        ExOrReItems.objects.create(
            exchange_or_return=exchange,
            order_item=order_item,
            quantity=order_item.quantity,
            is_active=True
        )
    
    return exchange

@transaction.atomic
def exchange_update(exchange_id, order_id, order_item_ids, user_id, reason, status, purpose, is_active):
    """
    Update an exchange/return request
    """
    exchange = get_exchange_by_id(exchange_id)
    
    order = Order.objects.get(id=order_id)
    user = User.objects.get(id=user_id)
    
    # Parse order item IDs
    if isinstance(order_item_ids, str):
        item_ids = [int(id.strip()) for id in order_item_ids.split(',') if id.strip()]
    else:
        item_ids = order_item_ids or []
    
    # Calculate new total
    total = 0
    order_items = []
    for item_id in item_ids:
        try:
            order_item = OrderItem.objects.select_related('product').get(id=item_id, order=order)
            order_items.append(order_item)
            total += order_item.product.price * order_item.quantity
        except OrderItem.DoesNotExist:
            continue
    
    # Update exchange
    exchange.order = order
    exchange.user = user
    exchange.reason = reason
    exchange.total = total
    exchange.status = int(status)
    exchange.purpose = int(purpose)
    exchange.is_active = is_active
    
    # Update processed date if status changes to approved/rejected
    if int(status) in [ExchangeOrReturnStatus.APPROVED.value, ExchangeOrReturnStatus.REJECTED.value]:
        exchange.processed_date = timezone.now()
    
    exchange.save()
    
    # Update items - delete old and create new
    exchange.exchange_return_items.all().delete()
    
    for order_item in order_items:
        ExOrReItems.objects.create(
            exchange_or_return=exchange,
            order_item=order_item,
            quantity=order_item.quantity,
            is_active=True
        )
    
    return exchange

def toggle_active_exchange(exchange_id, is_active):
    exchange = get_exchange_by_id(exchange_id)
    exchange.is_active = bool(is_active)
    exchange.save()
    return exchange

def get_all_unassigned_exchanges():
    return ExchangeOrReturn.objects.filter(
        status=ExchangeOrReturnStatus.PENDING.value, 
        is_active=True
    ).select_related('order', 'user').prefetch_related('exchange_return_items__order_item__product')

def get_exchange_data_by_order(order):
    return ExchangeOrReturn.objects.filter(
        order=order, 
        is_active=True
    ).first()

def get_exchange_or_return(pickup):
    return ExchangeOrReturn.objects.filter(
        order=pickup.order, 
        is_active=True
    ).first()