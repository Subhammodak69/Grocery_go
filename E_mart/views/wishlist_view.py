from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from E_mart.services import wishlist_service
from E_mart.constants.decorators import enduser_required



@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(enduser_required, name='dispatch')
class ToggleWishlistCreateDelete(View):
    def post(self, request, product_id):
        in_wishlist = wishlist_service.toggle_wishlist_create_delete(product_id, request.user)
        return JsonResponse({'message': "success", 'in_wishlist': in_wishlist})


class CheckWishlistStatus(View):
    def get(self, request, product_id):
        user = request.user
        in_wishlist = wishlist_service.is_in_wishlist(product_id, user)
        return JsonResponse({'in_wishlist': in_wishlist})