from django.views import View
from django.shortcuts import render,redirect
from E_mart.services import product_service,cart_service,order_service,payment_service,delivery_service,deliveryperson_service
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required,admin_required,delivery_worker_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from E_mart.constants.default_values import OrderStatus,DeliveryStatus,Purpose



@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name= 'dispatch')
class ProductOrderSummary(View):
    def get(self, request):
        product_id = request.GET.get('product_id')
        quantity = request.GET.get('quantity')
        product = product_service.get_product_data_by_id(product_id)
        product.update({
            'quantity':quantity,
            'is_selected_quantity_available':product_service.is_product_in_stock(product['id'],quantity)
        })
        total = product['original_price']* int(product['quantity'])
        total_discount = (product['original_price']-product['price'])*int(product['quantity'])
        extra_data = {
            'total':total,
            'delivery_fee': order_service.get_delivery_fee(total),
            'discount': total_discount
        }
        final_price = (total-total_discount)+extra_data['delivery_fee']
        return render(request, 'enduser/singly_order_summary.html', {'total_price':final_price,'data': product,'extra_data':extra_data})
    
    def post(self, request):
        try:

            # Extract form data from POST request
            user = request.user
            product_details_id = request.POST.get('product_details_id')
            address = request.POST.get('address', '').strip()
            quantity = request.POST.get('quantity', '1').strip()
            listing_price = request.POST.get('listing_price')
            delivery_fee = request.POST.get('delivery_fee')
            discount = request.POST.get('discount')

            quantity = int(quantity)
            if not address:
                return render(request, 'enduser/singly_order_summary.html', {
                    'error_message': 'Address is required',
                })

            product_is_available = product_service.is_product_in_stock(product_details_id, quantity)
            if not product_is_available:
                return render(request, 'enduser/success_delay_redirect.html', {'redirected_url':'/','message':'Product is recently out of stock!','status':'error'})
            # Create order using your service function
            order = order_service.sigle_order_create(user, product_details_id, address, quantity, listing_price, delivery_fee, discount)
            payment_data = request.session.get('payment_data')
            payment = payment_service.api_create_payment(order,payment_data)
            if not payment:
                return  render(request, 'enduser/success_delay_redirect.html', {'redirected_url':f"/create/payment/{order.id}/",'message':'Payment failed! Redirecting...','status':'error'})
            request.session.pop('payment_data')
            if order:
                return render(request, 'enduser/success_delay_redirect.html', {'redirected_url':f"/order/{order.id}/",'message':'Order placed successfully! Redirecting...','status':'success'})

            else:
                return render(request, 'enduser/success_delay_redirect.html', {'redirected_url':'/','message':'Failed to create order','status':'error'})
        except Exception as e:
            render(request, 'enduser/success_delay_redirect.html', {'redirected_url':'/','message':'Server Error!','status':'error'})

    
@method_decorator(enduser_required, name='dispatch')
class ProductsOrderSummaryByCart(View):
    def get(self,request):
        user_cart = cart_service.get_cart_by_user(request.user.id)
        products_data = cart_service.get_all_cart_products_data(user_cart)
        if not products_data:
            return redirect('/user/cart/')
        summary = cart_service.get_cart_summary(user_cart)

        return render(request, 'enduser/cart_order_summary.html',{
            'cart_id':user_cart.id,
            'products_data':products_data, 
            'total_data':summary,
            }
        )
    
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name='dispatch')
class OrderCreateView(View):
    def post(self, request):
        try:
            import json
            data = json.loads(request.body)
            address = data.get('address', '').strip()
            final_price = data.get('final_price')
            delivery_fee = data.get('delivery_fee')
            discount = data.get('discount')

            if not address:
                return JsonResponse({
                    'success': False,
                    'message': 'Address is required'
                })

            order = order_service.create_order(request.user, address, final_price, delivery_fee, discount)
            
            if order:
                payment_data = request.session.get('payment_data')
                res = payment_service.api_create_payment(order,payment_data)
                if not res:
                    order.delete()
                    return JsonResponse({'success':False, 'message':'server error!'})
                request.session.pop('payment_data')
                return JsonResponse({
                    'success': True,
                    'message': 'Order created successfully',
                    'order_id': order.id,  # return this for frontend redirect
                    'redirect_url': f'/order/{order.id}/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Product is out of stock or cart is empty!'
                })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
        
@method_decorator(enduser_required, name='dispatch')
class OrderListView(View):
    def get(self, request):
        orders = order_service.get_all_orders_by_user(request.user)
        context = {
            'orders': orders
        }
        return render(request, 'enduser/orders.html', context)   
    
@method_decorator(enduser_required, name='dispatch')
class OrderDetailsView(View):
    def get(self, request,order_id):
        order_data = order_service.get_order_full_data(order_id)
        if not order_data:
            return redirect('/orders/')
        summary = order_service.get_order_price_summary(order_id) 
        payment = payment_service.get_payment_data_by_order_id(order_id)
        context = {
            'order_data': order_data,
            'summary':summary,
            'payment':payment
        }
        return render(request, 'enduser/order_details.html', context)   

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name='dispatch')
class OrderDeleteView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            if not order_id:
                return JsonResponse({'error': 'Order ID not provided'}, status=400)

            order_service.delete_order(order_id, request.user)

            return JsonResponse({'message': 'Order cancelled successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
                

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name='dispatch')
class OrderPermanentDeleteView(View):
    def post(self, request, order_id):
        try:
            if not order_id:
                return JsonResponse({'error': 'Order ID not provided'}, status=400)

            order = order_service.get_order_by_id(order_id)
            orderitems = order_service.get_orderitems_by_order_id(order_id)
            for item in orderitems:
                product = item.product
                product.stock += item.quantity
                product.save()
            order.delete()
            return JsonResponse({'message': 'Order deleted successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    

#For Admin View

@method_decorator(admin_required,name='dispatch')
class AdminOrderListView(View):
    def get(self, request):
        filter_value = request.GET.get('filter', None)
        if filter_value == 'pending':
            filter_by = 'PENDING'
        elif filter_value == 'processing':
            filter_by = 'PROCESSING'
        elif filter_value == 'outfordelivery':
            filter_by = 'OUTFORDELIVERY'
        elif filter_value == 'delivered':
            filter_by = 'DELIVERED'
        elif filter_value == 'cancelled':
            filter_by = 'CANCELLED'
        elif filter_value == 'confirmed':
            filter_by = 'CONFIRMED'
        else:
            filter_by = 'all'

        orders = order_service.get_all_orders(filter_by)
        orders_data = [
            {
                'order':order,
                'items_count':order.items.count(),
                'status_name':OrderStatus(order.status).name,
                'assigned_to':delivery_service.get_delivery_person_by_order(order.id)
            }
            for order in orders
        ]
        deliveryboys = deliveryperson_service.get_available_delivery_boys()
        context = {'orders': orders_data,'deliveryboys':deliveryboys}
        return render(request, 'admin/order/list.html', context)
    

@method_decorator(admin_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class AdminOrderAssignedView(View):
    def post(self, request):
        data = json.loads(request.body)
        order_id = data.get('order_id')
        assigned_to = data.get('assigned_to')
        if not all([order_id,assigned_to]):
            return JsonResponse({'success':False, 'message':'Order id or assigned_to is missing!'})
        res = delivery_service.assigned_worker(order_id,assigned_to)
        if res:
            order = order_service.get_order_by_id(order_id)
            order.status = OrderStatus.CONFIRMED.value
            order.save()
            return JsonResponse({'success':True, 'message':'Assigned successfully!'})
        return JsonResponse({'success':False, 'message':'Assigned is failed!'})
    
@method_decorator(delivery_worker_required, name='dispatch')
class DeliveryOrderDetails(View):
    def get(self,request,order_id):
        order = order_service.get_order_by_id(order_id)
        delivery = delivery_service.get_all_delivery_by_order(order)
        context = {
            "order": order,
            "delivery": delivery
        }
        return render(request, "delivery/order_details.html", context)
    
@method_decorator(delivery_worker_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class DeliveryOrPickupStatusUpdateView(View):
    def get(self, request, delivery_id):
        order_enums = order_service.get_order_enums()
        delivery = delivery_service.get_delivery_pickup_obj_by_id(delivery_id)
        status={
            'name':OrderStatus(delivery.order.status).name,
            'value':OrderStatus(delivery.order.status).value
        }
        data={
            'enums':order_enums,
            'status':status
        }
        return JsonResponse({'success':True,'data':data})
    
    def post(self, request, delivery_id):
        body_data = json.loads(request.body)
        status = int(body_data.get('status'))
                
        if not status:
            return JsonResponse({
                'success': False, 
                'data': {'message': 'No status provided'}
            }, status=400)
        
        try:
            
            status = delivery_service.update_delivery_or_pickup_status(delivery_id, status)
            return JsonResponse({
                'success': True, 
                'data': {'message': 'Status updated successfully','status':status}
            }) 
        except Exception as e:
            print("Update error:", str(e))
            return JsonResponse({
                'success': False, 
                'data': {'message': f'Error: {str(e)}'}
            }, status=500)
        
        