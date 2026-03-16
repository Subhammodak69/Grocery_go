# E_mart/services/admin_dashboard_service.py
from django.utils import timezone
from django.db.models import Sum, F, DecimalField
from datetime import timedelta
import json

from E_mart.models import User, Order, Category, OrderItem, DeliveryOrPickup, Payment,DeliveryPerson
from E_mart.constants.default_values import OrderStatus, DeliveryStatus, PaymentStatus, Role
from django.shortcuts import get_object_or_404
# Get today's date once for consistency
today = timezone.now().date()

def get_date_ranges():
    """Get various date ranges for filtering"""
    return {
        'today': today,
        'this_month_start': today.replace(day=1),
        'last_month_start': (today.replace(day=1) - timedelta(days=1)).replace(day=1),
        'last_month_end': today.replace(day=1) - timedelta(days=1),
    }

def get_total_orders():
    """Get total active orders"""
    return Order.objects.filter(is_active=True).count()

def get_orders_trend():
    """Calculate orders trend compared to last month"""
    dates = get_date_ranges()
    
    current_month_orders = Order.objects.filter(
        created_at__date__gte=dates['this_month_start'],
        is_active=True
    ).count()
    
    last_month_orders = Order.objects.filter(
        created_at__date__range=[dates['last_month_start'], dates['last_month_end']],
        is_active=True
    ).count()
    
    if last_month_orders > 0:
        trend = ((current_month_orders - last_month_orders) / last_month_orders) * 100
    else:
        trend = 100 if current_month_orders > 0 else 0
        
    return round(trend, 1)

def get_active_users():
    """Get count of active customer users"""
    return User.objects.filter(
        is_active=True, 
        role=Role.ENDUSER.value
    ).count()

def get_new_users_today():
    """Get count of new users registered today"""
    return User.objects.filter(
        date_joined__date=today,
        role=Role.ENDUSER.value
    ).count()

def get_monthly_revenue():
    """Get total revenue for current month"""
    current_month_start = get_date_ranges()['this_month_start']
    revenue = Payment.objects.filter(
        order__is_active=True,
        status=PaymentStatus.COMPLETED.value,
        created_at__date__gte=current_month_start
    ).aggregate(total=Sum('amount'))['total']
    return revenue or 0

def get_revenue_target():
    """Calculate revenue target (20% increase from last month)"""
    dates = get_date_ranges()
    last_month_revenue = Payment.objects.filter(
        order__is_active=True,
        status=PaymentStatus.COMPLETED.value,
        created_at__date__range=[dates['last_month_start'], dates['last_month_end']]
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    return float(last_month_revenue) * 1.2 if last_month_revenue > 0 else 10000

def get_pending_deliveries():
    """Get count of pending deliveries"""
    return DeliveryOrPickup.objects.filter(
        status=DeliveryStatus.PENDING.value,
        is_active=True
    ).count()

def get_overdue_deliveries():
    """Get count of overdue deliveries"""
    return DeliveryOrPickup.objects.filter(
        status=DeliveryStatus.PENDING.value,
        assigned_at__lt=timezone.now() - timedelta(hours=48),
        is_active=True
    ).count()

def get_weekly_orders():
    """Get orders for the last 7 days"""
    weekly_data = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = Order.objects.filter(
            created_at__date=date,
            is_active=True
        ).count()
        weekly_data.append(count)
    return weekly_data

def get_category_sales_data():
    """Get sales data by category"""
    categories = Category.objects.filter(is_active=True)
    category_names = []
    category_sales = []
    
    for category in categories:
        total = OrderItem.objects.filter(
            product__category=category,
            order__is_active=True,
            order__status__in=[OrderStatus.DELIVERED.value]
        ).aggregate(
            total=Sum(F('quantity') * F('product__price'), output_field=DecimalField())
        )['total'] or 0
        
        if total > 0:
            category_names.append(category.name)
            category_sales.append(float(total))
    
    return {
        'names': json.dumps(category_names),
        'values': json.dumps(category_sales)
    }

def get_recent_orders(limit=5):
    """Get recent orders with related data"""
    return Order.objects.select_related('user').filter(
        is_active=True
    ).order_by('-created_at')[:limit]

def get_all_dashboard_data():
    """Get all dashboard data in one call"""
    return {
        'total_orders': get_total_orders(),
        'orders_trend': get_orders_trend(),
        'active_users': get_active_users(),
        'new_users_today': get_new_users_today(),
        'monthly_revenue': get_monthly_revenue(),
        'revenue_target': get_revenue_target(),
        'pending_deliveries': get_pending_deliveries(),
        'overdue_deliveries': get_overdue_deliveries(),
        'weekly_orders': json.dumps(get_weekly_orders()),
        'category_names': get_category_sales_data()['names'],
        'category_sales': get_category_sales_data()['values'],
        'recent_orders': get_recent_orders(),
    }



def get_order_data(order_id):
    order = get_object_or_404(
        Order.objects.select_related('user'),
        id=order_id,
        is_active=True
    )

    order_items = OrderItem.objects.filter(
        order=order,
        is_active=True
    ).select_related('product')

    payment = Payment.objects.filter(order=order).first()

    delivery = DeliveryOrPickup.objects.filter(
        order=order,
        is_active=True
    ).select_related('delivery_person__user').first()

    available_delivery_persons = DeliveryPerson.objects.filter(
        is_available=True,
        is_active=True
    ).select_related('user')

    subtotal = sum(item.product.price * item.quantity for item in order_items)
    total_items = sum(item.quantity for item in order_items)

    return {
        'order': order,
        'order_items': order_items,
        'payment': payment,
        'delivery': delivery,
        'available_delivery_persons': available_delivery_persons,
        'subtotal': subtotal,
        'total_items': total_items,
        'status_choices': OrderStatus(order.status).name if order.status else '',
        'payment_status_choices': PaymentStatus(payment.status).name if payment.status else '',
        'delivery_status_choices': DeliveryStatus(delivery.status).name if delivery.status else '',
    }


def update_order_status(order_id, new_status):
    order = get_object_or_404(Order, id=order_id, is_active=True)

    old_status = order.status
    order.status = int(new_status)
    order.save()

    return old_status, order.status


def assign_delivery_person(order_id, person_id):
    order = get_object_or_404(Order, id=order_id, is_active=True)

    person = get_object_or_404(DeliveryPerson, id=int(person_id), is_active=True)

    delivery, created = DeliveryOrPickup.objects.update_or_create(
        order=order,
        defaults={
            'delivery_person': person,
            'address': order.delivery_address or order.user.address,
            'status': DeliveryStatus.ASSIGNED.value,
            'purpose': 1,
            'is_active': True
        }
    )

    person.is_available = False
    person.save()

    return delivery


def update_payment_status(payment_id, new_status):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = int(new_status)
    payment.save()


def cancel_order(order_id):
    order = get_object_or_404(Order, id=order_id, is_active=True)

    order.status = OrderStatus.CANCELLED.value
    order.save()

    for item in order.order_items.filter(is_active=True):
        product = item.product
        product.stock += item.quantity
        product.save()
