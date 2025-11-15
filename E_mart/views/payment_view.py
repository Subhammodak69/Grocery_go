from django.views import View
from django.shortcuts import render
from E_mart.services import payment_service,order_service
from E_mart.constants.decorators import enduser_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class PaymentCreateView(View):
    def get(self,request,order_id):
        order = order_service.get_order_by_id(order_id)
        return render(request,'enduser/payment.html',{'order':order})