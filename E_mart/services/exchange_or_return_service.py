from E_mart.models import ExchangeOrReturn,Order,OrderItem,ExOrReItems
from E_mart.services import order_service
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





#admin

def get_all_exchanges():
    return ExchangeOrReturn.objects.select_related('order', 'user').all()

def get_exchange_by_id(exchange_id):
    return ExchangeOrReturn.objects.select_related('order', 'user').get(id=exchange_id)

def exchange_create(order_id, order_item_id, user_id, product_id, reason, status, purpose, is_active):
    from E_mart.models import Order, OrderItem, User, Product
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.get(id=order_item_id)
    user = User.objects.get(id=user_id)
    product = Product.objects.get(id=product_id)
    
    exchange = ExchangeOrReturn.objects.create(
        order=order,
        order_item=order_item,
        user=user,
        reason=reason,
        status=int(status),
        purpose=int(purpose),
        is_active=is_active
    )
    return exchange

def exchange_update(exchange_id, order_id, order_item_id, user_id, product_id, reason, status, purpose, is_active):
    exchange = get_exchange_by_id(exchange_id)
    from E_mart.models import Order, OrderItem, User, Product
    order = Order.objects.get(id=order_id)
    user = User.objects.get(id=user_id)
    
    exchange.order = order
    exchange.user = user
    exchange.reason = reason
    exchange.status = int(status)
    exchange.purpose = int(purpose)
    exchange.is_active = is_active
    exchange.save()
    return exchange

def toggle_active_exchange(exchange_id, is_active):
    exchange = get_exchange_by_id(exchange_id)
    exchange.is_active = bool(is_active)
    exchange.save()
    return exchange


def get_all_unassigned_exchanges():
    return ExchangeOrReturn.objects.filter(status = ExchangeOrReturnStatus.PENDING.value, is_active = True)

def get_exchange_data_by_order(order):
    return ExchangeOrReturn.objects.filter(order = order,is_active = True).first()

def get_exchnage_or_return(pickup):
    return ExchangeOrReturn.objects.filter(order = pickup.order,is_active = True).first()