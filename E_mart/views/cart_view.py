from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from E_mart.services import cartitem_service,cart_service
import json
from E_mart.constants.decorators import enduser_required
from django.http import JsonResponse

@method_decorator(enduser_required, name='dispatch')
class UserCartDetailsView(View):
    def get(self, request):
        user = request.user
        user_cart = cart_service.get_cart_by_user(user)
        user_cart_data = cartitem_service.get_all_cartitems_by_cart(user_cart)
        total_summary_data = {
            "total_price": sum(item["product_price"] for item in user_cart_data)
        }
        return render(
            request,
            'enduser/cart.html',
            {
                'cart_id':user_cart.id,
                'cart_data': user_cart_data,
                'total_summary': total_summary_data
            }
        )

    
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name='dispatch')
class UserCartCreateDataView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        data = json.loads(request.body)
        product_details_id = data.get('product_details_id')
        quantity = data.get('quantity')
        user_cart = cart_service.get_cart_by_user(user)
        product_detail = cartitem_service.create_cartitem(user_cart,product_details_id,quantity)

        return JsonResponse({'status': 'success'})
    

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name='dispatch')
class ApiRemoveCartItem(View):
    def post(self, request, cart_id):
        try:
            data = json.loads(request.body)
            item_id = data.get('itemId')
            if not item_id:
                return JsonResponse({'error': 'No itemId provided.'}, status=400)

            # Assume cart_service.remove_item_from_cart(item_id) returns True on success, False otherwise
            print("hello world")
            res = cart_service.remove_item_from_cart(item_id)
            print(res,"output for remove")
            if res:
                return JsonResponse({'success': True, 'message': 'Item removed from cart.'}, status=200)
            else:
                return JsonResponse({'success': False, 'error': 'Could not remove item.'}, status=400)
        except Exception as e:
            # Log the exception (best practice for production)
            print(f'Error removing item from cart: {e}')
            return JsonResponse({'success': False, 'error': 'Internal Server Error.'}, status=500)
