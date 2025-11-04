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
        summary = cart_service.get_cart_summary(user_cart)
        return render(
            request,
            'enduser/cart.html',
            {
                'cart_id':user_cart.id,
                'cart_data': user_cart_data,
                'total_summary': summary,
            }
        )

    
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name='dispatch')
class UserCartCreateDataView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        user_cart = cart_service.get_cart_by_user(user)
        cartitem_service.create_cartitem(user_cart,product_id,quantity)
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
            res = cart_service.remove_item_from_cart(item_id)
            if res:
                return JsonResponse({'success': True, 'message': 'Item removed from cart.'}, status=200)
            else:
                return JsonResponse({'success': False, 'error': 'Could not remove item.'}, status=400)
        except Exception as e:
            # Log the exception (best practice for production)
            print(f'Error removing item from cart: {e}')
            return JsonResponse({'success': False, 'error': 'Internal Server Error.'}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name='dispatch')
class CartItemUpdateView(View):
    def post(self, request, item_id):
        data = json.loads(request.body)
        quantity = data.get('quantity')

        cart_item,summary = cart_service.update_cart_items_quantity(item_id,request.user,quantity)
        print(summary)
        return JsonResponse({
            "cart_item_id": cart_item.id,
            "quantity": cart_item.quantity,
            "item_total": cart_service.get_cartitem_total_by_item_id(cart_item.id),
            "cart_summary": summary,
        })