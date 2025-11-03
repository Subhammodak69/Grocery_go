from django.views import View
from django.shortcuts import render,redirect
from E_mart.services import product_service,cart_service,order_service
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name= 'dispatch')
class ProductOrderSummary(View):
    def get(self, request):
        product_id = request.GET.get('product_id')
        quantity = request.GET.get('quantity')
        product = product_service.get_product_data_by_id(product_id)
        print(product)
        product.update({
            'quantity':quantity
        })
        total = product['price']* int(product['quantity'])
        extra_data = {
            'total':total,
            'delivery_fee': order_service.get_delivery_fee(total),
            'discount': order_service.get_discount_for_sigle_item(total)
        }
        final_price = total+extra_data['delivery_fee']-extra_data['discount']
        # print(extra_data)
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

            if not discount:
                discount = 0.00
            if not address:
                return JsonResponse({
                    'success': False,
                    'message': 'Address is required'
                })

            if not product_details_id or not quantity.isdigit():
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid product or quantity'
                })

            quantity = int(quantity)
            
            # Create order using your service function
            order = order_service.sigle_order_create(user,product_details_id, address, quantity,listing_price,delivery_fee,discount)
            
            if order:
                return redirect(f'/order/{order.id}')
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
class ProductsOrderSummaryByCart(View):
    def get(self,request):
        user_cart = cart_service.get_cart_by_user(request.user.id)
        products_data = cart_service.get_all_cart_products_data(user_cart)
        summary = cart_service.get_cart_summary(user_cart)
        
        return render(request, 'enduser/cart_order_summary.html',{
            'cart_id':user_cart.id,
            'products_data':products_data, 
            'total_data':summary,
            'final_price': summary['total_price']+summary['fee']-summary['discount']
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
                    'redirect_url': f'/order/{order.id}/'
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
        print(orders)
        context = {
            'orders': orders
        }
        return render(request, 'enduser/orders.html', context)   
    
@method_decorator(enduser_required, name='dispatch')
class OrderDetailsView(View):
    def get(self, request,order_id):
        order_data = order_service.get_order_full_data(order_id)
        summary = order_service.get_order_price_summary(order_id) 

        context = {
            'order_data': order_data,
            'summary':summary
        }
        print(order_data)
        return render(request, 'enduser/order_details.html', context)   