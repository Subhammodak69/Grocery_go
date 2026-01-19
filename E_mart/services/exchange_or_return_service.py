from E_mart.models import ExchangeOrReturn,Order,OrderItem
from E_mart.services import order_service
from E_mart.constants.default_values import ExchangeOrReturnStatus,ExOrRePurpose

def create_exchange_or_return(*, order_id, order_item_ids, user, purpose, reason):
    order = Order.objects.get(id=order_id)

    for item_id in order_item_ids:
        order_item = OrderItem.objects.get(id=item_id)

        ExchangeOrReturn.objects.create(
            order=order,
            order_item=order_item,
            user=user,
            product=order_item.product,
            reason=reason,
            purpose=int(purpose)
        )

def get_all_exchanges_or_returns_by_user(user):
    exchanges_or_returns = ExchangeOrReturn.objects.filter(user=user).order_by('-request_date')
    exchanges_or_returns_data = [
        {
            'id': item.id,
            'total': item.order.total_price,
            'status': ExchangeOrReturnStatus(item.status).name,
            'status_value': ExchangeOrReturnStatus(item.status).value,
            'address': item.order.delivery_address,
            'purpose':ExOrRePurpose(item.purpose).name,
            'request_date': item.request_date,
            'orderitems': order_service.get_order_items_data(item.order)
        }
        for item in exchanges_or_returns
    ]
    return exchanges_or_returns_data

def get_exchange_return_by_id_for_user(pickup_id, user):
    return (
        ExchangeOrReturn.objects
        .select_related('order', 'user', 'order_item', 'product')
        .filter(id=pickup_id, user=user)
        .first()
    )





#admin

def get_all_exchanges():
    return ExchangeOrReturn.objects.select_related('order', 'order_item', 'user', 'product').all()

def get_exchange_by_id(exchange_id):
    return ExchangeOrReturn.objects.select_related('order', 'order_item', 'user', 'product').get(id=exchange_id)

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
        product=product,
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
    order_item = OrderItem.objects.get(id=order_item_id)
    user = User.objects.get(id=user_id)
    product = Product.objects.get(id=product_id)
    
    exchange.order = order
    exchange.order_item = order_item
    exchange.user = user
    exchange.product = product
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



