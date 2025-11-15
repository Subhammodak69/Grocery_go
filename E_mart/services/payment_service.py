from E_mart.models import Payment
from E_mart.services import order_service
from E_mart.constants.default_values import PaymentStatus,PaymentMethod

def check_order_is_paid(order_id):
    order = order_service.get_order_by_id(order_id)
    return Payment.objects.filter(order = order,status = PaymentStatus.PENDING.value and PaymentStatus.FAILED.value).exclude(method =PaymentMethod.COD.value ).exists()