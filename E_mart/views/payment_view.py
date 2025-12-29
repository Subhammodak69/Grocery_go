from django.views import View
from django.shortcuts import render,redirect
from E_mart.services import payment_service,order_service
from E_mart.constants.decorators import enduser_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse
from decimal import Decimal



@method_decorator(enduser_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class PaymentCreateView(View):
    def get(self,request,order_id):
        order = order_service.get_order_by_id(order_id)
        is_paid =payment_service.check_order_is_paid(order.id)
        if is_paid:
            return redirect('/')
        return render(request,'enduser/payment.html',{'order':order})

    def post(self, request,order_id):
        try:
            data = json.loads(request.body)
            payment_method = data.get('method')
            amount = Decimal(data.get('amount'))
            order = order_service.get_order_by_id(order_id)
            if not amount == order.total_price:
                return JsonResponse({'success':False,'error':"Invalid Amount! Try again."}, status=500)
            # Validate payment method
            if payment_method not in ['UPI', 'CREDITCARD', 'DEBITCARD', 'NETBANKING', 'COD']:
                return JsonResponse({'success': False, 'error': 'Invalid payment method'}, status=400)

            # Payment data validation
            if payment_method == 'UPI':
                upi_id = data.get('upi_id')
                if not upi_id:
                    return JsonResponse({'success': False, 'error': 'UPI ID is required'}, status=400)

            elif payment_method in ['CREDITCARD', 'DEBITCARD']:
                card_number = data.get('card_number')
                expiry = data.get('expiry')
                cvv = data.get('cvv')
                if not (card_number and expiry and cvv):
                    return JsonResponse({'success': False, 'error': 'Complete card details required'}, status=400)

            elif payment_method == 'NETBANKING':
                bank = data.get('bank')
                if not bank:
                    return JsonResponse({'success': False, 'error': 'Bank selection required'}, status=400)
            
            payment_service.create_payment(order,data)

            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@method_decorator(enduser_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class ApiPaymentCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        request.session['payment_data'] = data
        return JsonResponse({'success':True})