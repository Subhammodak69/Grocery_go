from E_mart.models import ExchangeOrReturn,Order,OrderItem
from E_mart.services import order_service
from E_mart.constants.default_values import ExchangeOrReturnStatus

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
