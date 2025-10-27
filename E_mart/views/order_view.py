from django.views import View
from django.shortcuts import render,redirect
from E_mart.services import product_service,cart_service,order_service
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name= 'dispatch')
class ProductOrderSummary(View):
    def get(self, request):
        product_details_id = request.GET.get('product_details_id')
        quantity = request.GET.get('quantity')
        product_data = product_service.product_all_data_by_details_id(product_details_id)
        product_data.update({
            'quantity':quantity
        })
        total_price = product_data['price']* int(product_data['quantity'])
        
        return render(request, 'enduser/singly_order_summary.html', {'total_price':total_price,'data': product_data})
    
    def post(self, request):
        try:
            # Extract form data from POST request
            user = request.user
            product_details_id = request.POST.get('product_details_id')
            address = request.POST.get('address', '').strip()
            quantity = request.POST.get('quantity', '1').strip()

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
            order = order_service.sigle_order_create(user, product_details_id, address, quantity)
            
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
        total_summary_data = {
            'total_price': sum(item['product_price'] for item in products_data)
        }
        print(user_cart)
        return render(request, 'enduser/cart_order_summary.html',{'cart_id':user_cart.id,'products_data':products_data, 'total_data':total_summary_data})
    
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name='dispatch')
class OrderCreateView(View):
    def post(self, request):
        try:
            import json
            data = json.loads(request.body)
            address = data.get('address', '').strip()
            
            if not address:
                return JsonResponse({
                    'success': False,
                    'message': 'Address is required'
                })
            
            # Create order with address
            order = order_service.create_order(request.user, address)
            
            if order:
                return JsonResponse({
                    'success': True,
                    'message': 'Order created successfully',
                    'redirect_url': f'/orders/{order.id}/'
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

