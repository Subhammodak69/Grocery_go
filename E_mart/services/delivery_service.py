from E_mart.models import Delivery

def get_all_delivery():
    return Delivery.objects.all()

def get_delivery_by_order_id(order):
    return Delivery.objects.filter(order = order, is_active = True)

def get_delivery(delivery_id):
    return Delivery.objects.get(id=delivery_id, is_active = True)

def create_delivery(order,delivery_person):
    return Delivery.objects.create(
        order = order,
        delivery_person = delivery_person,    
    )
    
def deactivate_delivery(delivery):
    delivery.is_active = False
    delivery.save()
    return delivery