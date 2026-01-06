from E_mart.models import Order,OrderItem

def get_orderitems_by_order(order):
    return OrderItem.objects.filter(order = order,is_active = True)