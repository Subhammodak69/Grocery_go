from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import admin_required
from E_mart.services import category_service
from django.http import JsonResponse
import json


@method_decorator(admin_required, name='dispatch')
class AdminCategoryListView(View):
    def get(self,request):
        categories = category_service.get_all_categories()
        print(categories)
        return render(request,'admin/category/category_list.html',{'categories':categories})
    
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminCategoryCreateView(View):
    def get(self,request):
        return render(request,'admin/category/category_create.html')
    
    def post(self, request):
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')  
        

            
            if not all([name,description,image_file]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            category_service.category_create(name, description, image_file)
            return JsonResponse({'message': 'category created successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminCategoryUpdateView(View):
    def get(self,request, category_id):
        category = category_service.get_category_by_id(category_id)
        return render(request,'admin/category/category_update.html',{'category':category})
    
    def post(self, request, category_id):
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            image_file = request.FILES.get('image', None)

           
            if not all([name,description]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            category_service.category_update(category_id,name, description, image_file)
            return JsonResponse({'message': 'category created successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
      
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminCategoryToggleActiveView(View):
    def post(self, request):
        print("hello")
        data = json.loads(request.body)
        is_active = data.get('is_active')
        category_id = data.get('category_id')
        print("going",category_id,is_active)
        category = category_service.toggle_active_category(category_id, is_active)
        print("category=>",category.is_active)
        return JsonResponse({
            'success': True,
            'category_id': category.id,
            'is_active': category.is_active
        })