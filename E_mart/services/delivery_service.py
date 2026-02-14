from E_mart.models import DeliveryOrPickup,DeliveryPerson,Order
from E_mart.services import order_service,deliveryperson_service,exchange_or_return_service,worker_service
from E_mart.constants.default_values import DeliveryStatus,Purpose,ExchangeOrReturnStatus
from django.utils import timezone
from datetime import timedelta
import datetime
from django.shortcuts import get_object_or_404
from django.db import models

def get_delivery_person_by_order(order):
    item = DeliveryOrPickup.objects.filter(order = order).first()
    assigned_by = None
    if item:
        assigned_by =item.delivery_person.id if item.delivery_person else None
    return assigned_by

def get_delivery_worker_obj_by_user_id(user):
    return DeliveryPerson.objects.get(user = user, is_active = True)

def assigned_worker(order_id,assigned_to):
    order = order_service.get_order_by_id(order_id)
    assigned_user = deliveryperson_service.get_delivery_person_by_id(assigned_to)
    if assigned_user:
        return DeliveryOrPickup.objects.create(
            order = order,
            address = order.delivery_address,
            delivery_person = assigned_user,
            status = DeliveryStatus.ASSIGNED.value,
            purpose = Purpose.DELIVERY.value,
            delivered_at = timezone.now()+timedelta(hours=24)
        )
    else:
        return False

def get_last_7_days_stats(worker):
    today = timezone.now().date()

    labels = []
    deliveries_counts = []
    pickups_counts = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime("%a"))

        deliveries_qs = DeliveryOrPickup.objects.filter(
            assigned_at__date=day,
            purpose=Purpose.DELIVERY.value,
            delivery_person = worker,
            status = DeliveryStatus.DELIVERED.value
        )
        pickups_qs = DeliveryOrPickup.objects.filter(
            assigned_at__date=day,
            purpose=Purpose.PICKUP.value,
            delivery_person = worker,
            status = DeliveryStatus.PICKEDUP.value
        )

        deliveries_counts.append(deliveries_qs.count())
        pickups_counts.append(pickups_qs.count())

    total_deliveries = sum(deliveries_counts)
    total_pickups = sum(pickups_counts)
    total_jobs = total_deliveries + total_pickups
    completion_rate = 0
    if total_jobs > 0:
        completion_rate = round((total_deliveries / total_jobs) * 100)

    return {
        "labels": labels,
        "deliveries": deliveries_counts,
        "pickups": pickups_counts,
        "total_deliveries": total_deliveries,
        "total_pickups": total_pickups,
        "completion_rate": completion_rate,
    }

def get_deliveries_by_deliveryPerson(worker):
    """
    Get active delivery orders assigned to a specific delivery person.
    Prefetches related order, order_items, and products for efficient template rendering.
    """
    deliveries = DeliveryOrPickup.objects.filter(
        delivery_person=worker,
        purpose=Purpose.DELIVERY.value,
        is_active=True
    ).exclude(
        status__in=[
            DeliveryStatus.DELIVERED.value,
            DeliveryStatus.FAILED.value
        ]
    ).prefetch_related(
        'order__order_items__product',
        'order__user'
    ).select_related('delivery_person__user', 'order').order_by('-assigned_at')
    statuses = [delivery.status for delivery in deliveries]
    print(statuses)
    return deliveries

def get_pickups_by_deliveryPerson(worker):
    """
    Get active delivery orders assigned to a specific delivery person.
    """
    pickups = DeliveryOrPickup.objects.filter(
        delivery_person=worker,
        purpose=Purpose.PICKUP.value,
        is_active=True
    ).exclude(
        status__in = [DeliveryStatus.PICKEDUP.value,DeliveryStatus.RETURNED.value,DeliveryStatus.DELIVERED.value]
    ).order_by('-assigned_at')
    
    # Convert to list and add data
    result = []
    for pickup in pickups:
        exchange_or_return = exchange_or_return_service.get_exchnage_or_return(pickup)
        exchange_or_return_items = exchange_or_return_service.get_exchnage_or_return_items(exchange_or_return)
        
        # Add as dict if you want serialized data
        pickup_data = {
            'pickup': pickup,
            'purpose':Purpose(pickup.purpose).name,
            'exchange_or_return': exchange_or_return,
            'request_date':exchange_or_return.request_date,
            'status':ExchangeOrReturnStatus(exchange_or_return.status).name,
            'total':exchange_or_return.total,
            'items': exchange_or_return_items
        }
        result.append(pickup_data)
    return result


def get_total_delivery_or_pickup_by_worker(worker):
    deliveries = DeliveryOrPickup.objects.filter(
        delivery_person=worker,
        status__in=[
            DeliveryStatus.DELIVERED.value,
            DeliveryStatus.PICKEDUP.value
        ]
    )

    return deliveries

def get_all_delivery_pickups_of_worker(worker):
    return DeliveryOrPickup.objects.filter(delivery_person = worker)

def get_total_complete_deliveries_of_worker(worker):
    return DeliveryOrPickup.objects.filter(
        delivery_person = worker,
        purpose = Purpose.DELIVERY.value,
        status = DeliveryStatus.DELIVERED.value
    )
def get_total_complete_pickups_of_worker(worker):
    return DeliveryOrPickup.objects.filter(
        delivery_person = worker,
        purpose = Purpose.PICKUP.value,
        status = DeliveryStatus.PICKEDUP.value
    )

def get_delivery_data_by_order(order):
    delivery = DeliveryOrPickup.objects.filter(order = order, is_active = True,purpose = Purpose.DELIVERY.value,).first()
    data={
        'id':delivery.id,
        'assigned_at':delivery.assigned_at,
        'delivered_at':delivery.delivered_at,
        'purpose':Purpose(delivery.purpose).name,
        'status_value':delivery.status,
        'status':DeliveryStatus(delivery.status).name
    }
    return data
def get_pickup_data_by_order(order):
    delivery = DeliveryOrPickup.objects.filter(order = order, is_active = True,purpose = Purpose.PICKUP.value,).first()
    data={
        'id':delivery.id,
        'assigned_at':delivery.assigned_at,
        'delivered_at':delivery.delivered_at,
        'purpose':Purpose(delivery.purpose).name,
        'status':DeliveryStatus(delivery.status).name
    }
    return data


def get_delivery_pickup_obj_by_id(id):
    return DeliveryOrPickup.objects.filter(id=id).first()

def update_delivery_or_pickup_status(id, status):
    delivery_pickup = DeliveryOrPickup.objects.filter(id = id,is_active = True).first()
    delivery_pickup.status = DeliveryStatus(status).value
    delivery_pickup.save()
    # print(DeliveryStatus(delivery_pickup.status).name)
    return DeliveryStatus(delivery_pickup.status).name


def get_all_deliveryorpickup_orders():
    return DeliveryOrPickup.objects.all()

def create_admin_pickups(exchange_id,assigned_to):
    exchnage = exchange_or_return_service.get_exchange_by_id(exchange_id)
    worker = worker_service.get_worker_obj(assigned_to)
    pickup = DeliveryOrPickup.objects.create(
        order = exchnage.order,
        delivery_person = worker,
        address = exchnage.order.delivery_address,
        status = DeliveryStatus.ASSIGNED.value,
        purpose = Purpose.PICKUP.value
    )
    exchnage.status = ExchangeOrReturnStatus.APPROVED.value
    exchnage.save()
    return pickup


def get_all_deliveries():
    return DeliveryOrPickup.objects.select_related('order', 'delivery_person').all()

def get_delivery_by_id(delivery_id):
    return get_object_or_404(DeliveryOrPickup, id=delivery_id)

def delivery_create(order_id, address, delivery_person_id, status, purpose, delivered_at, is_active):
    order = get_object_or_404(Order, id=order_id)
    delivery_person = get_object_or_404(DeliveryPerson, id=delivery_person_id) if delivery_person_id else None
    
    delivered_at_date = None
    if delivered_at:
        delivered_at_date = datetime.strptime(delivered_at, '%Y-%m-%dT%H:%M') if 'T' in delivered_at else None
    
    DeliveryOrPickup.objects.create(
        order=order,
        address=address,
        delivery_person=delivery_person,
        status=status,
        purpose=purpose,
        delivered_at=delivered_at_date,
        is_active=is_active
    )

def delivery_update(delivery_id, order_id, address, delivery_person_id, status, purpose, delivered_at, is_active):
    delivery = get_delivery_by_id(delivery_id)
    order = get_object_or_404(Order, id=order_id)
    delivery_person = get_object_or_404(DeliveryPerson, id=delivery_person_id) if delivery_person_id else None
    
    delivered_at_date = None
    if delivered_at:
        delivered_at = models.DateTimeField(null=True, blank=True)
    
    delivery.order = order
    delivery.address = address
    delivery.delivery_person = delivery_person
    delivery.status = status
    delivery.purpose = purpose
    delivery.delivered_at = delivered_at_date
    delivery.is_active = is_active
    delivery.save()
    return delivery

def toggle_active_delivery(delivery_id, is_active):
    delivery = get_delivery_by_id(delivery_id)
    delivery.is_active = is_active
    delivery.save()
    return delivery

def get_delivery_count_by_worker(user):
    delivery_person = DeliveryPerson.objects.get(user = user,is_active = True)
    return DeliveryOrPickup.objects.filter(delivery_person = delivery_person, is_active = True,purpose = Purpose.DELIVERY.value, status__in = [DeliveryStatus.ASSIGNED.value,DeliveryStatus.IN_PROGRESS.value,DeliveryStatus.FAILED.value] ).count()

def get_pickup_count_by_worker(user):
    delivery_person = DeliveryPerson.objects.get(user = user,is_active = True)
    return DeliveryOrPickup.objects.filter(delivery_person = delivery_person, is_active = True,purpose = Purpose.PICKUP.value, status__in = [DeliveryStatus.ASSIGNED.value,DeliveryStatus.IN_PROGRESS.value,DeliveryStatus.FAILED.value] ).count()
