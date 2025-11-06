from django.views import View
from django.shortcuts import redirect
from E_mart.services import review_service
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from E_mart.constants.decorators import enduser_required
import json

@method_decorator(enduser_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ReviewCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            photo = data.get('photo_url')
            text = data.get('review')
            stars = data.get('rating')

            review = review_service.create_review(product_id, request.user, text, photo, stars)

            return JsonResponse({'success': True, 'data': review})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
