from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from E_mart.constants.decorators import enduser_required,admin_required
from E_mart.services import order_service,orderitem_service,exchange_or_return_service,payment_service,user_service,product_service,deliveryperson_service,delivery_service
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

        return redirect('/exchanges-or-returns/')
    
class ExchangeReturnDetailsView(View):
    def get(self,request,pk):
        exchange_or_return = exchange_or_return_service.get_exchange_return_by_id_for_user(pk,request.user) 
        order_data = order_service.get_order_full_data(exchange_or_return.order.id)
        items = order_service.get_order_items_data(exchange_or_return.order)
        summary = order_service.get_price_summary(exchange_or_return.order)
        payment = payment_service.get_payment_data_by_order_id(exchange_or_return.order.id)
        return render(request, 'enduser/pickup_order_details.html', {
            'exchange_or_return': exchange_or_return,
            'order_data': order_data,
            'items': items,
            'summary': summary,
            'payment': payment,
        })
    


#admin

@method_decorator(admin_required, name='dispatch')
class AdminExchangeListView(View):
    def get(self, request):
        exchanges = exchange_or_return_service.get_all_exchanges() 
        return render(request, 'admin/exchange_request/exchange_list.html', {'exchanges': exchanges})

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminExchangeCreateView(View):
    def get(self, request):
        orders = order_service.get_all_orders()
        users = user_service.get_all_users()
        products = product_service.get_all_products()
        return render(request, 'admin/exchange_request/exchange_create.html', {
            'orders': orders, 'users': users, 'products': products
        })
    
    def post(self, request):
        try:
            order_id = request.POST.get('order')
            order_item_id = request.POST.get('order_item')
            user_id = request.POST.get('user')
            product_id = request.POST.get('product')
            reason = request.POST.get('reason')
            status = request.POST.get('status')
            purpose = request.POST.get('purpose')
            is_active = request.POST.get('is_active', 'true').lower() == 'true'

            if not all([order_id, order_item_id, user_id, product_id, reason, status, purpose]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            exchange_or_return_service.exchange_create(
                order_id, order_item_id, user_id, product_id, reason, 
                status, purpose, is_active
            )
            return JsonResponse({'message': 'Exchange request created successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminExchangeUpdateView(View):
    def get(self, request, exchange_id):
        exchange = exchange_or_return_service.get_exchange_by_id(exchange_id)
        orders = order_service.get_all_orders()
        users = user_service.get_all_users()
        products = product_service.get_all_products()
        return render(request, 'admin/exchange_request/exchange_update.html', {
            'exchange': exchange, 'orders': orders, 'users': users, 'products': products
        })
    
    def post(self, request, exchange_id):
        try:
            order_id = request.POST.get('order')
            order_item_id = request.POST.get('order_item')
            user_id = request.POST.get('user')
            product_id = request.POST.get('product')
            reason = request.POST.get('reason')
            status = request.POST.get('status')
            purpose = request.POST.get('purpose')
            is_active = request.POST.get('is_active', 'true').lower() == 'true'

            exchange_or_return_service.exchange_update(
                exchange_id, order_id, order_item_id, user_id, product_id, 
                reason, status, purpose, is_active
            )
            return JsonResponse({'message': 'Exchange request updated successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminExchangeToggleActiveView(View):
    def post(self, request):
        data = json.loads(request.body)
        is_active = data.get('is_active')
        exchange_id = data.get('exchange_id')
        exchange = exchange_or_return_service.toggle_active_exchange(exchange_id, is_active)
        return JsonResponse({
            'success': True,
            'exchange_id': exchange.id,
            'is_active': exchange.is_active
        })

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class GetOrderItemsView(View):
    def get(self, request, order_id):
        items = order_service.get_order_items(order_id)
        return JsonResponse(items, safe=False)
    

@method_decorator(admin_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class AdminPickupsAssignedView(View):
    def get(self,request):
        exchanges = exchange_or_return_service.get_all_unassigned_exchanges() 
        workers = deliveryperson_service.get_available_delivery_boys()
        workers_data = [
            {
                'id':worker.id,
                'full_name':f"{worker.user.first_name} {worker.user.last_name}"
            }
            for worker in workers
        ]
        return render(request,'admin/order/unassigned_pickups.html',{'exchanges':exchanges,'workers':workers_data})
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            exchange_id = data.get('exchange_id')
            assigned_to = data.get('assigned_to')
            if not all([exchange_id,assigned_to]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            pickups = delivery_service.create_admin_pickups(exchange_id,assigned_to)
            return JsonResponse({'success':True, 'message':"Assinged Successfully"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        