from django.views import View
from django.shortcuts import render,redirect
from E_mart.services import product_service,cart_service,order_service
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json



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
        print(request.user.id)
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
                return render(request, 'enduser/singly_order_summary.html', {
                    'error_message': 'Product is recently out of stock',
                })

            # Create order using your service function
            order = order_service.sigle_order_create(user, product_details_id, address, quantity, listing_price, delivery_fee, discount)

            if order:
                return redirect(f'/create/payment/{order.id}/')
            else:
                return render(request, 'enduser/singly_order_summary.html', {
                    'error_message': 'Failed to create order',
                })
        except Exception as e:
            return render(request, 'enduser/singly_order_summary.html', {
                'error_message': str(e),
            })

    
@method_decorator(enduser_required, name='dispatch')
class ProductsOrderSummaryByCart(View):
    def get(self,request):
        user_cart = cart_service.get_cart_by_user(request.user.id)
        products_data = cart_service.get_all_cart_products_data(user_cart)
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
            
            # Create order with address
            order = order_service.create_order(request.user, address,final_price,delivery_fee,discount)
            
            if order:
                return JsonResponse({
                    'success': True,
                    'message': 'Order created successfully',
                    'redirect_url': f'/create/payment/{order.id}/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Failed to create order'
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

        context = {
            'order_data': order_data,
            'summary':summary
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