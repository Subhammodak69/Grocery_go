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
                'cart_data': user_cart_data,
                'total_summary': total_summary_data
            }
        )

    
@method_decorator(csrf_exempt, name='dispatch')
class UserCartCreateDataView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        data = json.loads(request.body)
        product_details_id = data.get('product_details_id')
        quantity = data.get('quantity')
        user_cart = cart_service.get_cart_by_user(user)
        product_detail = cartitem_service.create_cartitem(user_cart,product_details_id,quantity)

        return JsonResponse({'status': 'success'})