from E_mart.models import Payment
from E_mart.services import order_service
from E_mart.constants.default_values import PaymentStatus,PaymentMethod,OrderStatus

def check_order_is_paid(order_id):
    order = order_service.get_order_by_id(order_id)
    return Payment.objects.filter(
        order=order,
    ).exclude(
        status__in=[PaymentStatus.PENDING.value, PaymentStatus.FAILED.value]
    ).exclude(
        method=PaymentMethod.COD.value
    ).exists()

def create_payment(order, payment_data):
    method_str = payment_data.get('method')
    # Map string method to PaymentMethod enum value
    method_map = {
        'COD': PaymentMethod.COD.value,
        'UPI': PaymentMethod.UPI.value,
        'CREDITCARD': PaymentMethod.CREDITCARD.value,
        'DEBITCARD': PaymentMethod.DEBITCARD.value,
        'NETBANKING': PaymentMethod.NETBANKING.value,
    }
    method = method_map.get(method_str)

    # Prepare payment fields conditionally based on method
    card_details = None
    bank_details = None
    upi_id = None

    if method_str in ['CREDITCARD', 'DEBITCARD']:
        card_number = payment_data.get('card_number', '')
        expiry = payment_data.get('expiry', '')
        # Mask card details except last 4 digits
        masked_card = "**** **** **** " + (card_number[-4:] if len(card_number) >= 4 else '')
        card_details = f"{masked_card} Expiry: {expiry}"
    elif method_str == 'NETBANKING':
        bank_details = payment_data.get('bank')
    elif method_str == 'UPI':
        upi_id = payment_data.get('upi_id')

    is_paid_in_cod = Payment.objects.filter(order=order, method=PaymentMethod.COD.value).first()

    if is_paid_in_cod:
        try:
            payment = Payment.objects.filter(order=order, is_active=True).first()
            if payment:
                payment.status = PaymentStatus.COMPLETED.value
                payment.card_details = card_details
                payment.bank_details = bank_details
                payment.upi_id = upi_id
                payment.amount = payment_data.get('amount')
                payment.transaction_id = payment_data.get('transaction_id')
                payment.method = method  # removed trailing comma that made it a tuple
                payment.save()
            else:
                print("DEBUG: No active payment found to update.")
        except Exception as e:
            print(f"ERROR saving payment update for COD payment: {e}")
    else:
        try:
            payment = Payment.objects.create(
                user=order.user,
                order=order,
                method=method,
                card_details=card_details,
                bank_details=bank_details,
                upi_id=upi_id,
                amount=payment_data.get('amount'),
                transaction_id=payment_data.get('transaction_id')
            )
            if payment:
                payment.status = PaymentStatus.PENDING.value if method == PaymentMethod.COD.value else PaymentStatus.COMPLETED.value
                payment.save()

            order.status = OrderStatus.PROCESSING.value
            order.save()

        except Exception as e:
            print(f"ERROR creating new payment: {e}")

    return payment


def get_payment_data_by_order_id(order_id):
    order = order_service.get_order_by_id(order_id)
    return Payment.objects.filter(order = order, is_active = True).first()

def api_create_payment(order, payment_data):    
    # Get method from payment_data
    method_str = payment_data.get('method')
    
    # Map string method to PaymentMethod enum value
    method_map = {
        'COD': PaymentMethod.COD.value,
        'UPI': PaymentMethod.UPI.value,
        'CREDITCARD': PaymentMethod.CREDITCARD.value,
        'DEBITCARD': PaymentMethod.DEBITCARD.value,
        'NETBANKING': PaymentMethod.NETBANKING.value,
    }
    method = method_map.get(method_str)
    
    # Validate method
    if not method:
        raise ValueError(f"Invalid payment method: {method_str}")
    
    # Get payment_details object (nested data)
    payment_details = payment_data.get('payment_details', {})
    
    # Prepare payment fields conditionally based on method
    card_details = None
    bank_details = None
    upi_id = None
    transaction_id = payment_data.get('transaction_id')  # May be None initially
    
    if method_str in ['CREDITCARD', 'DEBITCARD']:
        card_number = payment_details.get('card_number', '')
        expiry = payment_details.get('expiry', '')
        cvv = payment_details.get('cvv', '')
        # Mask card details except last 4 digits
        masked_card = "**** **** **** " + (card_number[-4:] if len(card_number) >= 4 else '')
        card_details = f"{masked_card} Expiry: {expiry}"
        
    elif method_str == 'NETBANKING':
        bank_details = payment_details.get('bank')
        
    elif method_str == 'UPI':
        upi_id = payment_details.get('upi_id')  # ← Get from payment_details
    
    # Check if there's an existing COD payment to update
    is_paid_in_cod = Payment.objects.filter(
        order=order, 
        method=PaymentMethod.COD.value
    ).first()
    
    if is_paid_in_cod:
        # Update existing COD payment
        try:
            payment = Payment.objects.filter(order=order, is_active=True).first()
            if payment:
                payment.status = PaymentStatus.COMPLETED.value
                payment.card_details = card_details
                payment.bank_details = bank_details
                payment.upi_id = upi_id
                payment.amount = payment_data.get('amount')
                payment.transaction_id = transaction_id
                payment.method = method
                payment.save()
                print(f"DEBUG: Updated COD payment {payment.id} to {method_str}")
            else:
                print("DEBUG: No active payment found to update.")
        except Exception as e:
            print(f"ERROR saving payment update for COD payment: {e}")
            raise
    else:
        # Create new payment
        try:
            payment = Payment.objects.create(
                user=order.user,
                order=order,
                method=method,
                card_details=card_details,
                bank_details=bank_details,
                upi_id=upi_id,
                amount=payment_data.get('amount'),
                transaction_id=transaction_id,
                status=PaymentStatus.PENDING.value if method == PaymentMethod.COD.value else PaymentStatus.COMPLETED.value
            )
            
            print(f"DEBUG: Created new payment {payment.id} - Method: {method_str}, Amount: {payment.amount}")
            
            # Update order status
            order.status = OrderStatus.PROCESSING.value
            order.save()
            
        except Exception as e:
            print(f"ERROR creating new payment: {e}")
            raise
    
    return payment


def get_payment_data_by_order(order):
    payment = Payment.objects.filter(order = order, is_active = True).first()
    data = {
        'id':payment.id,
        'status':PaymentStatus(payment.status).name,
        'method':PaymentMethod(payment.method).name,
        'amount':payment.amount,
        'created_at':payment.created_at,
        'transaction_id':payment.transaction_id
    }
    return data

