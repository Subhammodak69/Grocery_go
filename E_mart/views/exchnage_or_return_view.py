from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from E_mart.constants.decorators import enduser_required,admin_required
from E_mart.services import order_service,orderitem_service,exchange_or_return_service,payment_service,user_service,product_service,deliveryperson_service,delivery_service
import json
from E_mart.constants.default_values import ExchangeOrReturnStatus

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

@method_decorator(enduser_required,name='dispatch')
class ExchangeReturnDetailsView(View):
    def get(self,request,pk):
        exchange_or_return = exchange_or_return_service.get_exchange_return_by_id_for_user(pk,request.user) 
        items = exchange_or_return_service.get_exchnage_or_return_items(exchange_or_return) 
        address = exchange_or_return.order.delivery_address
        return render(request, 'enduser/pickup_order_details.html', {
            'exchange_or_return': exchange_or_return,
            'items': items,
            'address':address
        })
    

@method_decorator(admin_required, name='dispatch')
class AdminExchangeListView(View):
    def get(self, request):
        exchanges = exchange_or_return_service.get_all_exchanges()
        orders = order_service.get_all_orders()
        users = user_service.get_all_users()
        enums = [
            {
                'name': i.name,
                'value': i.value
            }
            for i in ExchangeOrReturnStatus
        ]
        return render(request, 'admin/exchange_list.html', {
            'exchanges': exchanges,
            'orders': orders,
            'users': users,
            'enums': enums
        })

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminExchangeCreateView(View):
    def post(self, request):
        try:
            order_id = request.POST.get('order')
            order_item_ids = request.POST.getlist('order_items[]') or request.POST.get('order_items')
            user_id = request.POST.get('user')
            reason = request.POST.get('reason')
            status = request.POST.get('status')
            purpose = request.POST.get('purpose')
            is_active = request.POST.get('is_active', 'true').lower() == 'true'

            if not all([order_id, user_id, reason, status, purpose]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            if not order_item_ids:
                return JsonResponse({'error': 'At least one order item is required'}, status=400)

            exchange = exchange_or_return_service.exchange_create(
                order_id, order_item_ids, user_id, reason, 
                status, purpose, is_active
            )
            
            # Get items for response
            items = []
            for item in exchange.exchange_return_items.all():
                items.append({
                    'id': item.id,
                    'product_name': item.order_item.product.name,
                    'quantity': item.quantity
                })
            
            return JsonResponse({
                'success': True,
                'message': 'Exchange request created successfully!',
                'exchange': {
                    'id': exchange.id,
                    'order_id': exchange.order.id,
                    'user_name': exchange.user.username,
                    'reason': exchange.reason[:50] + '...' if len(exchange.reason) > 50 else exchange.reason,
                    'status': exchange.status,
                    'status_display': exchange.get_status_display(),
                    'purpose': exchange.purpose,
                    'purpose_display': exchange.get_purpose_display(),
                    'total': str(exchange.total),
                    'request_date': exchange.request_date.strftime('%Y-%m-%d %H:%M:%S') if exchange.request_date else None,
                    'is_active': exchange.is_active,
                    'items': items
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminExchangeDetailView(View):
    def get(self, request, exchange_id):
        try:
            exchange = exchange_or_return_service.get_exchange_by_id(exchange_id)
            
            # Get all orders for dropdown
            orders = order_service.get_all_orders()
            orders_list = []
            for order in orders:
                orders_list.append({
                    'id': order.id,
                    'display': f"Order #{order.id} - {order.user.username} (₹{order.total_price})"
                })
            
            # Get all users for dropdown
            users = user_service.get_all_users()
            users_list = []
            for user in users:
                users_list.append({
                    'id': user.id,
                    'display': f"{user.username} ({user.email})"
                })
            
            # Get order items for the selected order with selection status
            order_items_list = []
            selected_item_ids = [item.order_item.id for item in exchange.exchange_return_items.all()]
            
            if exchange.order:
                items = order_service.get_order_items(exchange.order.id)
                for item in items:
                    order_items_list.append({
                        'id': item['id'],
                        'product_name': item['product_name'],
                        'quantity': item['quantity'],
                        'price': item['price'],
                        'selected': item['id'] in selected_item_ids
                    })
            
            # Get exchange items
            exchange_items = []
            for item in exchange.exchange_return_items.all():
                exchange_items.append({
                    'id': item.id,
                    'order_item_id': item.order_item.id,
                    'product_name': item.order_item.product.name,
                    'quantity': item.quantity,
                    'price': str(item.order_item.product.price)
                })
            
            # Get status enums
            enums_list = []
            for i in ExchangeOrReturnStatus:
                enums_list.append({
                    'name': i.name,
                    'value': i.value
                })
            
            exchange_data = {
                'id': exchange.id,
                'order_id': exchange.order.id if exchange.order else None,
                'user_id': exchange.user.id if exchange.user else None,
                'reason': exchange.reason,
                'total': str(exchange.total),
                'status': exchange.status,
                'status_display': exchange.get_status_display(),
                'purpose': exchange.purpose,
                'purpose_display': exchange.get_purpose_display(),
                'request_date': exchange.request_date.strftime('%Y-%m-%d %H:%M:%S') if exchange.request_date else None,
                'processed_date': exchange.processed_date.strftime('%Y-%m-%d %H:%M:%S') if exchange.processed_date else None,
                'is_active': exchange.is_active,
                'orders_list': orders_list,
                'users_list': users_list,
                'order_items_list': order_items_list,
                'exchange_items': exchange_items,
                'enums_list': enums_list,
                'selected_item_ids': selected_item_ids
            }
            return JsonResponse(exchange_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminExchangeUpdateView(View):
    def post(self, request, exchange_id):
        try:
            order_id = request.POST.get('order')
            order_item_ids = request.POST.getlist('order_items[]') or request.POST.get('order_items')
            user_id = request.POST.get('user')
            reason = request.POST.get('reason')
            status = request.POST.get('status')
            purpose = request.POST.get('purpose')
            is_active = request.POST.get('is_active', 'true').lower() == 'true'

            if not all([order_id, user_id, reason, status, purpose]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            if not order_item_ids:
                return JsonResponse({'error': 'At least one order item is required'}, status=400)

            exchange = exchange_or_return_service.exchange_update(
                exchange_id, order_id, order_item_ids, user_id, 
                reason, status, purpose, is_active
            )
            
            # Get items for response
            items = []
            for item in exchange.exchange_return_items.all():
                items.append({
                    'id': item.id,
                    'product_name': item.order_item.product.name,
                    'quantity': item.quantity
                })
            
            return JsonResponse({
                'success': True,
                'message': 'Exchange request updated successfully!',
                'exchange': {
                    'id': exchange.id,
                    'order_id': exchange.order.id,
                    'user_name': exchange.user.username,
                    'reason': exchange.reason[:50] + '...' if len(exchange.reason) > 50 else exchange.reason,
                    'status': exchange.status,
                    'status_display': exchange.get_status_display(),
                    'purpose': exchange.purpose,
                    'purpose_display': exchange.get_purpose_display(),
                    'total': str(exchange.total),
                    'request_date': exchange.request_date.strftime('%Y-%m-%d %H:%M:%S') if exchange.request_date else None,
                    'is_active': exchange.is_active,
                    'items': items
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminExchangeToggleActiveView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            is_active = data.get('is_active')
            exchange_id = data.get('exchange_id')
            exchange = exchange_or_return_service.toggle_active_exchange(exchange_id, is_active)
            return JsonResponse({
                'success': True,
                'exchange_id': exchange.id,
                'is_active': exchange.is_active
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class GetOrderItemsView(View):
    def get(self, request, order_id):
        try:
            items = order_service.get_order_items(order_id)
            return JsonResponse(items, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)