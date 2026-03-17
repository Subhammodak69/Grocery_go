from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import admin_required
from E_mart.services import poster_service, product_service
import json
import os

@method_decorator(admin_required, name='dispatch')
class AdminPosterListView(View):
    def get(self, request):
        posters = poster_service.get_all_posters()
        products = product_service.get_all_active_products()
        return render(request, 'admin/poster_list.html', {
            'posters': posters,
            'products': products
        })

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterCreateView(View):
    def post(self, request):
        try:
            product_id = request.POST.get('product_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            if not all([product_id, title, image_file, start_date, end_date]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            poster = poster_service.poster_create(
                product_id, title, description, image_file, start_date, end_date
            )
            
            # Get the created poster with related data
            poster_data = {
                'id': poster.id,
                'title': poster.title,
                'description': poster.description,
                'image': poster.image,
                'start_date': poster.start_date.isoformat() if poster.start_date else None,
                'end_date': poster.end_date.isoformat() if poster.end_date else None,
                'is_active': poster.is_active,
                'product_id': poster.product_id,
                'product_name': poster.product.name if poster.product else None,
                'created_at': poster.created_at.isoformat() if poster.created_at else None
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Poster created successfully!',
                'poster': poster_data
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterDetailView(View):
    def get(self, request, poster_id):
        try:
            poster = poster_service.get_poster_by_id(poster_id)
            poster_data = {
                'id': poster.id,
                'title': poster.title,
                'description': poster.description,
                'image': poster.image,
                'start_date': poster.start_date.isoformat() if poster.start_date else None,
                'end_date': poster.end_date.isoformat() if poster.end_date else None,
                'is_active': poster.is_active,
                'product_id': poster.product_id,
                'product_name': poster.product.name if poster.product else None,
                'created_at': poster.created_at.isoformat() if poster.created_at else None
            }
            return JsonResponse(poster_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterUpdateView(View):
    def post(self, request, poster_id):
        try:
            product_id = request.POST.get('product_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            if not all([product_id, title, description, start_date, end_date]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            poster = poster_service.poster_update(
                poster_id, product_id, title, description, image_file, start_date, end_date
            )
            
            poster_data = {
                'id': poster.id,
                'title': poster.title,
                'description': poster.description,
                'image': poster.image,
                'start_date': poster.start_date.isoformat() if poster.start_date else None,
                'end_date': poster.end_date.isoformat() if poster.end_date else None,
                'is_active': poster.is_active,
                'product_id': poster.product_id,
                'product_name': poster.product.name if poster.product else None,
                'created_at': poster.created_at.isoformat() if poster.created_at else None
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Poster updated successfully!',
                'poster': poster_data
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterToggleActiveView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            is_active = data.get('is_active')
            poster_id = data.get('poster_id')
            poster = poster_service.toggle_active_poster(poster_id, is_active)
            return JsonResponse({
                'success': True,
                'poster_id': poster.id,
                'is_active': poster.is_active
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)