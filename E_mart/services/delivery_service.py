
from E_mart.models import DeliveryOrPickup,DeliveryPerson
from E_mart.services import order_service,deliveryperson_service
from E_mart.constants.default_values import DeliveryStatus,Purpose
from django.utils import timezone
from datetime import timedelta

def get_delivery_person_by_order(order):
    item = DeliveryOrPickup.objects.filter(order = order).first()
    assigned_by = None
    if item:
        assigned_by =item.delivery_person.id if item.delivery_person else None
    return assigned_by

def assigned_worker(order_id,assigned_to):
    order = order_service.get_order_by_id(order_id)
    assigned_user = deliveryperson_service.get_delivery_person_by_id(assigned_to)
    return DeliveryOrPickup.objects.create(
        order = order,
        address = order.delivery_address,
        delivery_person = assigned_user,
        status = DeliveryStatus.ASSIGNED.value,
        purpose = Purpose.DELIVERY.value,
        delivered_at = timezone.now()+timedelta(hours=24)
    )