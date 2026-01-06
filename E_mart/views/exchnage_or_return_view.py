from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from E_mart.constants.decorators import enduser_required
from E_mart.services import order_service,orderitem_service,exchange_or_return_service,payment_service
import json

@method_decorator(enduser_required,name='dispatch')
class ExchangeReturnListView(View):
    def get(self, request):
        pickups = exchange_or_return_service.get_all_exchanges_or_returns_by_user(request.user)

        return render(request, 'enduser/pickups.html',{'pickups':pickups})

@method_decorator(enduser_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class ExchangeReturnCreateView(View):    
    def get(self, request, order_id):
        order = order_service.get_order_by_id(order_id)
        order_items = orderitem_service.get_orderitems_by_order(order)
        
        context = {
            'order': order,
            'order_items':order_items
        }
        print(context)
        return render(request,'enduser/exchange_or_return.html', context)

    def post(self, request, order_id):
        order_items = request.POST.getlist('order_items[]')
        purpose = request.POST.get('purpose')
        reason = request.POST.get('reason')

        exchange_or_return_service.create_exchange_or_return(
            order_id=order_id,
            order_item_ids=order_items,
            user=request.user,
            purpose=purpose,
            reason=reason
        )

        return redirect(request.path)
    
class ExchangeReturnDetailsView(View):
    def get(self,request,pk):
        exchange_or_return = exchange_or_return_service.get_exchange_return_by_id_for_user(pk,request.user) 
        order_data = order_service.get_order_full_data(exchange_or_return.order.id)
        items = order_service.get_order_items_data(exchange_or_return.order)
        print(items)
        summary = order_service.get_price_summary(exchange_or_return.order)
        payment = payment_service.get_payment_data_by_order_id(exchange_or_return.order.id)
        return render(request, 'enduser/pickup_order_details.html', {
            'exchange_or_return': exchange_or_return,
            'order_data': order_data,
            'items': items,
            'summary': summary,
            'payment': payment,
        })
        