from E_mart.models import DeliveryOrPickup,DeliveryPerson,ExchangeOrReturn
from E_mart.services import order_service,deliveryperson_service
from E_mart.constants.default_values import DeliveryStatus,Purpose,OrderStatus
from django.utils import timezone
from datetime import timedelta

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
    return DeliveryOrPickup.objects.create(
        order = order,
        address = order.delivery_address,
        delivery_person = assigned_user,
        status = DeliveryStatus.ASSIGNED.value,
        purpose = Purpose.DELIVERY.value,
        delivered_at = timezone.now()+timedelta(hours=24)
    )

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
    ).prefetch_related(
        'order__order_items__product',
        'order__user'
    ).select_related('delivery_person__user', 'order').order_by('-assigned_at')
    
    return deliveries

def get_pickups_by_deliveryPerson(worker):
    """
    Get active delivery orders assigned to a specific delivery person.
    Prefetches related order, order_items, and products for efficient template rendering.
    """
    pickups = DeliveryOrPickup.objects.filter(
        delivery_person=worker,
        purpose=Purpose.PICKUP.value,
        is_active=True
    ).prefetch_related(
        'order__order_items__product',
        'order__user'
    ).select_related('delivery_person__user', 'order').order_by('-assigned_at')
    
    return pickups

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

def get_all_delivery_by_order(order):
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

def get_delivery_pickup_obj_by_id(id):
    return DeliveryOrPickup.objects.filter(id=id).first()

def update_delivery_or_pickup_status(id, status):
    delivery = DeliveryOrPickup.objects.filter(id=id).first()
    delivery.order.status = OrderStatus(status).value
    delivery.order.save()
    if(delivery.order.status == OrderStatus.CANCELLED.value):
        delivery.status = DeliveryStatus.FAILED.value
        delivery.save()
    elif(delivery.order.status == OrderStatus.CONFIRMED.value):
        delivery.status = DeliveryStatus.ASSIGNED.value
        delivery.save()
    elif(delivery.order.status == OrderStatus.OUTFORDELIVERY.value):
        delivery.status = DeliveryStatus.IN_PROGRESS.value
        delivery.save()
    elif(delivery.order.status == OrderStatus.DELIVERED.value):
        delivery.status = DeliveryStatus.DELIVERED.value
        delivery.save()
    else:
        pass
    status=DeliveryStatus(delivery.status).name
    return status