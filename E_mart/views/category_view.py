# views/admin_views.py
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import admin_required
from E_mart.services import category_service
from django.http import JsonResponse
import json
import os
from django.conf import settings


@method_decorator(admin_required, name='dispatch')
class AdminCategoryManagementView(View):
    """Single page for all category management operations"""
    
    def get(self, request):
        categories = category_service.get_all_categories()
        return render(request, 'admin/category/category_list.html', {'categories': categories})


@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminCategoryCreateAPIView(View):
    """API endpoint for creating categories"""
    
    def post(self, request):
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')
            
            # Validate required fields
            if not name:
                return JsonResponse({'error': 'Category name is required'}, status=400)
            
            if not image_file:
                return JsonResponse({'error': 'Category image is required'}, status=400)

            # Create category
            category = category_service.category_create(name, description, image_file)
            
            return JsonResponse({
                'success': True,
                'message': 'Category created successfully!',
                'category': {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'image': category.image,
                    'is_active': category.is_active
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminCategoryUpdateAPIView(View):
    """API endpoint for updating categories"""
    
    def post(self, request, category_id):
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            image_file = request.FILES.get('image', None)

            # Validate required fields
            if not name:
                return JsonResponse({'error': 'Category name is required'}, status=400)
            
            if not description:
                return JsonResponse({'error': 'Category description is required'}, status=400)

            # Update category
            category = category_service.category_update(category_id, name, description, image_file)
            
            return JsonResponse({
                'success': True,
                'message': 'Category updated successfully!',
                'category': {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'image': category.image,
                    'is_active': category.is_active
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminCategoryToggleActiveView(View):
    """API endpoint for toggling category active status"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            is_active = data.get('is_active')
            category_id = data.get('category_id')
            
            if category_id is None or is_active is None:
                return JsonResponse({'error': 'Category ID and status are required'}, status=400)
            
            category = category_service.toggle_active_category(category_id, is_active)
            
            return JsonResponse({
                'success': True,
                'category_id': category.id,
                'is_active': category.is_active
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(admin_required, name='dispatch')
class AdminCategoryDetailAPIView(View):
    """API endpoint for getting category details"""
    
    def get(self, request, category_id):
        try:
            category = category_service.get_category_by_id(category_id)
            
            if not category:
                return JsonResponse({'error': 'Category not found'}, status=404)
            
            # Get created_at if available (add this field to your Category model if needed)
            created_at = None
            if hasattr(category, 'created_at') and category.created_at:
                created_at = category.created_at.strftime('%B %d, %Y')
            
            data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'image': category.image,
                'is_active': category.is_active,
                'created_at': created_at,
            }
            return JsonResponse(data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)
    
def ApiGetAllCategory(request):
    categories = category_service.get_category_data()
    return JsonResponse({'categories': categories})