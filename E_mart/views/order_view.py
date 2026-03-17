from django.views import View
from django.shortcuts import render,redirect
from E_mart.services import product_service,cart_service,order_service,payment_service,delivery_service,deliveryperson_service,user_service,exchange_or_return_service
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required,admin_required,delivery_worker_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from E_mart.constants.default_values import OrderStatus,DeliveryStatus,ExchangeOrReturnStatus



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
        order = order_service.get_order_by_id(order_id)
        payment = payment_service.get_payment_data_by_order(order)
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
        
        
@method_decorator(delivery_worker_required, name='dispatch')
class DeliveryOrderDetails(View):
    def get(self,request,order_id):
        order = order_service.get_order_by_id(order_id)
        delivery = delivery_service.get_delivery_data_by_order(order)
        context = {
            "order": order,
            "delivery": delivery
        }
        return render(request, "delivery/delivery_order_details.html", context)
    
@method_decorator(delivery_worker_required, name='dispatch')
class PickupOrderDetails(View):
    def get(self, request, order_id):
        order = order_service.get_order_by_id(order_id)
        pickup = delivery_service.get_pickup_data_by_order(order)
        exchange_data = exchange_or_return_service.get_exchange_data_by_order(order)
        
        context = {
            "order_data": order,
            "pickup": pickup,
            "exchange": exchange_data,
            "items": exchange_data.exchange_return_items.all() if exchange_data else [],
            "user": exchange_data.user if exchange_data else None,
            "address": order.delivery_address if order else "",
        }
        return render(request, "delivery/pickup_order_details.html", context)
    
@method_decorator(delivery_worker_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class DeliveryStatusUpdateView(View):
    def get(self, request, delivery_id):
        delivery_enums = order_service.get_order_enums_for_delivery()
        delivery = delivery_service.get_delivery_pickup_obj_by_id(delivery_id)
        status={
            'name':OrderStatus(delivery.status).name,
            'value':OrderStatus(delivery.status).value
        }
        data={
            'enums':delivery_enums,
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
            delivery = delivery_service.get_delivery_by_id(delivery_id)
            status = delivery_service.update_delivery_or_pickup_status(delivery_id, status)
            if(status == 'IN_PROGRESS'):
                delivery.order.status = OrderStatus.OUTFORDELIVERY.value
                delivery.order.save()
            elif(status == 'DELIVERED'):
                is_paid = payment_service.check_payment_done_or_not_by_order(delivery.order)
                print(is_paid)
                if not is_paid:
                    print("go to payment")
                    payment_service.create_COD_payment(delivery.order) 
                delivery.order.status = OrderStatus.DELIVERED.value
                delivery.order.save()
            elif(status == 'FAILED'):
                delivery.order.status = OrderStatus.FAILED.value
                delivery.order.save()
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
        
        
@method_decorator(delivery_worker_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class PickupStatusUpdateView(View):
    def get(self, request, pickup_id):  # Changed from order_id to pickup_id
        print("Pickup status enums loaded")
        
        # Get pickup object (assuming you have this service method)
        pickup = delivery_service.get_delivery_pickup_obj_by_id(pickup_id)
        
        # Get pickup status enums (similar to your delivery enums)
        pickup_enums = order_service.get_enums_for_pickup() # or order_service.get_pickup_enums()
        
        # Format current status like your example
        status = {
            'name': DeliveryStatus(pickup.status).name,  # Use your actual enum class
            'value': DeliveryStatus(pickup.status).value
        }
        
        data = {
            'enums': pickup_enums,
            'status': status
        }
        
        return JsonResponse({'success': True, 'data': data})

        
    def post(self, request, pickup_id):
        body_data = json.loads(request.body)
        status = int(body_data.get('status'))
                
        if not status:
            return JsonResponse({
                'success': False, 
                'data': {'message': 'No status provided'}
            }, status=400)
        
        try:
            pickup = delivery_service.get_delivery_by_id(pickup_id)
            exchange_or_return = exchange_or_return_service.get_exchnage_or_return(pickup)
            status = delivery_service.update_delivery_or_pickup_status(pickup_id, status)
            if(status == 'IN_PROGRESS'):
                exchange_or_return.status = ExchangeOrReturnStatus.IN_PROGRESS.value
                exchange_or_return.save()
            elif(status == 'PICKEDUP'):
                exchange_or_return.status = ExchangeOrReturnStatus.EXCHANGED.value
                exchange_or_return.save()
            elif(status == 'FAILED'):
                exchange_or_return.status = ExchangeOrReturnStatus.REJECTED.value
                exchange_or_return.save()
            elif(status == 'RETURNED'):
                exchange_or_return.status = ExchangeOrReturnStatus.RETURNED.value
                exchange_or_return.save()
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
        

# ==================== ALL ORDERS MANAGEMENT (Full CRUD) ====================

@method_decorator(admin_required, name='dispatch')
class AdminOrderListView(View):
    def get(self, request):
        orders = order_service.get_all_orders()
        users = user_service.get_all_users()
        products = product_service.get_all_active_products()
        order_statuses = order_service.get_all_order_status()
        deliveryboys = deliveryperson_service.get_available_delivery_boys()
        
        # Prepare orders data with additional info
        orders_data = []
        for order in orders:
            # This now returns a DeliveryOrPickup object or None
            delivery_item = delivery_service.get_delivery_person_by_order(order.id)
            
            # Safely get the assigned person's name
            assigned_to_name = None
            assigned_to_id = None
            
            if delivery_item and delivery_item.delivery_person:
                assigned_to_name = delivery_item.delivery_person.user.get_full_name() if delivery_item.delivery_person.user else None
                assigned_to_id = delivery_item.delivery_person.id
            
            orders_data.append({
                'order': order,
                'items_count': order.items.count(),
                'status_name': OrderStatus(order.status).name,
                'assigned_to': assigned_to_name,
                'assigned_to_id': assigned_to_id
            })
        
        context = {
            'orders': orders_data,
            'users': users,
            'products': products,
            'order_statuses': order_statuses,
            'deliveryboys': deliveryboys
        }
        return render(request, 'admin/order_list.html', context)


@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminOrderCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            status = data.get('status')
            total_price = data.get('total_price')
            discount = data.get('discount', 0)
            delivery_fee = data.get('delivery_fee')
            listing_price = data.get('listing_price')
            delivery_address = data.get('delivery_address', '')
            is_active = data.get('is_active', True)
            items = data.get('items', [])

            if not all([user_id, status, total_price, delivery_fee, listing_price]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            order = order_service.order_create(
                user_id, status, total_price, discount, 
                delivery_fee, listing_price, delivery_address, is_active, items
            )
            
            # Return created order data for dynamic update
            order_data = {
                'id': order.id,
                'user_name': order.user.get_full_name() or order.user.username,
                'status': order.status,
                'status_display': OrderStatus(order.status).name,
                'total_price': str(order.total_price),
                'delivery_fee': str(order.delivery_fee),
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'items_count': order.items.count(),
                'is_active': order.is_active
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Order created successfully!',
                'order': order_data
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminOrderDetailView(View):
    def get(self, request, order_id):
        try:
            order = order_service.get_order_by_id(order_id)
            
            if not order:
                return JsonResponse({'error': 'Order not found'}, status=404)
            
            # Get order items - using order_items related_name from OrderItem model
            items = []
            for item in order.order_items.filter(is_active=True):  # Use order_items instead of items
                items.append({
                    'id': item.id,
                    'product_id': item.product.id,
                    'product_name': item.product.name,  # Fixed: removed extra .product
                    'product_image': item.product.image,
                    'size': item.product.size,
                    'quantity': item.quantity,
                    'price': str(item.product.price),  # Price comes from Product
                    'original_price': str(item.product.original_price)
                })
            
            # Get assigned delivery person
            assigned_to = delivery_service.get_delivery_person_by_order(order.id)
            
            order_data = {
                'id': order.id,
                'user_id': order.user.id,
                'user_name': order.user.get_full_name() or order.user.username,
                'user_email': order.user.email,
                'user_phone': order.user.phone_number,
                'status': order.status,
                'status_display': OrderStatus(order.status).name if hasattr(OrderStatus, '__call__') else OrderStatus(order.status).name,
                'total_price': str(order.total_price),
                'discount': str(order.discount),
                'delivery_fee': str(order.delivery_fee),
                'listing_price': str(order.listing_price),
                'delivery_address': order.delivery_address,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S') if order.updated_at else None,
                'is_active': order.is_active,
                'items': items,
                'items_count': len(items),  # Changed to use len(items) instead of order.items.count()
                'assigned_to': {
                    'id': assigned_to.id if assigned_to else None,
                    'name': assigned_to.delivery_person.user.get_full_name() if assigned_to and assigned_to.delivery_person.user else None
                } if assigned_to else None
            }
            return JsonResponse(order_data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminOrderUpdateView(View):
    def post(self, request, order_id):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            status = data.get('status')
            total_price = data.get('total_price')
            discount = data.get('discount', '0.00')
            delivery_fee = data.get('delivery_fee')
            listing_price = data.get('listing_price')
            delivery_address = data.get('delivery_address', '')
            is_active = data.get('is_active', True)
            current_items = data.get('current_items', [])
            new_items = data.get('new_items', [])

            if not all([user_id, status, total_price, delivery_fee, listing_price]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            order = order_service.order_update(
                order_id, user_id, status, total_price, discount, 
                delivery_fee, listing_price, delivery_address, is_active, 
                current_items, new_items
            )
            
            # Return updated order data
            order_data = {
                'id': order.id,
                'user_name': order.user.get_full_name() or order.user.username,
                'status': order.status,
                'status_display': OrderStatus(order.status).name,
                'total_price': str(order.total_price),
                'delivery_fee': str(order.delivery_fee),
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'items_count': order.items.count(),
                'is_active': order.is_active
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Order updated successfully!',
                'order': order_data
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminOrderToggleActiveView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            is_active = data.get('is_active')
            order_id = data.get('order_id')
            order = order_service.toggle_active_order(order_id, is_active)
            return JsonResponse({
                'success': True,
                'order_id': order.id,
                'is_active': order.is_active
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminOrderDeleteView(View):
    def post(self, request, order_id):
        try:
            success = order_service.delete_order(order_id)
            if success:
                return JsonResponse({
                    'success': True,
                    'message': 'Order deleted successfully!'
                })
            return JsonResponse({'error': 'Failed to delete order'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# ==================== UNASSIGNED ORDERS ====================

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminUnassignedOrdersView(View):
    def get(self, request):
        orders = order_service.get_all_unassigned_orders()
        workers = deliveryperson_service.get_available_delivery_boys()
        
        orders_data = []
        if orders:
            for order in orders:
                orders_data.append({
                    'id': order.id,
                    'delivery_address': order.delivery_address,
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': OrderStatus(order.status).name,
                    'is_active': order.is_active,
                    'customer_name': f"{order.user.first_name} {order.user.last_name}".strip() or order.user.username,
                    'customer_phone': order.user.phone_number,
                    'total_price': str(order.total_price),
                    'items_count': order.items.count()
                })
        
        workers_data = []
        if workers:
            for worker in workers:
                workers_data.append({
                    'id': worker.id,
                    'full_name': worker.user.get_full_name() if worker.user else "Unknown",
                    'is_available': worker.is_available
                })
        
        return render(request, 'admin/unassigned_order_list.html', {
            'orders': orders_data,
            'workers': workers_data
        })
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            assigned_to = data.get('assigned_to')
            
            if not all([order_id, assigned_to]):
                return JsonResponse({'success': False, 'message': 'Order ID or assigned_to is missing!'})
            
            res = delivery_service.assign_worker(order_id, assigned_to)
            if res:
                # Update order status to CONFIRMED
                order = order_service.get_order_by_id(order_id)
                order.status = OrderStatus.CONFIRMED.value
                order.save()
                
                # Get updated order and worker data for response
                worker = deliveryperson_service.get_delivery_person_by_id(assigned_to)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Assigned successfully!',
                    'order_id': order_id,
                    'assigned_to': {
                        'id': assigned_to,
                        'name': worker.user.get_full_name() if worker and worker.user else "Unknown"
                    }
                })
            
            return JsonResponse({'success': False, 'message': 'Assignment failed!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


# ==================== UNASSIGNED PICKUPS (Exchanges/Returns) ====================

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminUnassignedPickupsView(View):
    def get(self, request):
        # Get all unassigned exchanges/returns
        from E_mart.services import exchange_or_return_service
        
        exchanges = exchange_or_return_service.get_all_unassigned_exchanges()
        workers = deliveryperson_service.get_available_delivery_boys()
        
        exchanges_data = []
        if exchanges:
            for exchange in exchanges:
                exchanges_data.append({
                    'id': exchange.id,
                    'order_id': exchange.order.id,
                    'user_name': exchange.user.get_full_name() or exchange.user.username,
                    'reason': exchange.reason,
                    'status': exchange.get_status_display(),
                    'status_value': exchange.status,
                    'purpose': exchange.get_purpose_display(),
                    'request_date': exchange.request_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_active': exchange.is_active,
                    'product_name': exchange.product.name if exchange.product else 'N/A',
                    'product_image': exchange.product.image if exchange.product else None
                })
        
        workers_data = []
        if workers:
            for worker in workers:
                workers_data.append({
                    'id': worker.id,
                    'full_name': worker.user.get_full_name() if worker.user else "Unknown",
                    'is_available': worker.is_available
                })
        
        return render(request, 'admin/unassigned_pickups.html', {
            'exchanges': exchanges_data,
            'workers': workers_data
        })
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            exchange_id = data.get('exchange_id')
            assigned_to = data.get('assigned_to')
            
            if not all([exchange_id, assigned_to]):
                return JsonResponse({'success': False, 'message': 'Exchange ID or assigned_to is missing!'})
            
            from E_mart.services import exchange_or_return_service
            res = exchange_or_return_service.assign_pickup_worker(exchange_id, assigned_to)
            
            if res:
                # Get updated exchange and worker data
                worker = deliveryperson_service.get_delivery_person_by_id(assigned_to)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Pickup assigned successfully!',
                    'exchange_id': exchange_id,
                    'assigned_to': {
                        'id': assigned_to,
                        'name': worker.user.get_full_name() if worker and worker.user else "Unknown"
                    }
                })
            
            return JsonResponse({'success': False, 'message': 'Assignment failed!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


# ==================== FILTERED ORDERS VIEW ====================

@method_decorator(admin_required, name='dispatch')
class AdminFilteredOrdersView(View):
    def get(self, request):
        filter_value = request.GET.get('filter', None)
        filter_map = {
            'pending': 'PENDING',
            'processing': 'PROCESSING',
            'outfordelivery': 'OUTFORDELIVERY',
            'delivered': 'DELIVERED',
            'cancelled': 'CANCELLED',
            'confirmed': 'CONFIRMED'
        }
        
        filter_by = filter_map.get(filter_value, 'all')
        orders = order_service.get_all_orders(filter_by)
        
        orders_data = []
        for order in orders:
            assigned_to = delivery_service.get_delivery_person_by_order(order.id)
            orders_data.append({
                'order': order,
                'items_count': order.items.count(),
                'status_name': OrderStatus(order.status).name,
                'assigned_to': assigned_to.user.get_full_name() if assigned_to and assigned_to.user else None,
                'assigned_to_id': assigned_to.id if assigned_to else None
            })
        
        deliveryboys = deliveryperson_service.get_available_delivery_boys()
        
        return render(request, 'admin/order/filtered_orders.html', {
            'orders': orders_data,
            'deliveryboys': deliveryboys,
            'current_filter': filter_value
        })