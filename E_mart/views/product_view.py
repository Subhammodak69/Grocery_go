from django.views import View
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import admin_required,enduser_required
from E_mart.services import product_service,category_service
from django.http import JsonResponse
import json


@method_decorator(admin_required, name='dispatch')
class AdminProductListView(View):
    def get(self,request):
        products = product_service.get_all_products()
        return render(request,'admin/product/product_list.html',{'products':products})
    
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminProductCreateView(View):
    def get(self,request):
        categories = category_service.get_all_active_categories()
        return render(request,'admin/product/product_create.html',{'categories':categories})
    
    def post(self, request):
        try:
            category_id = request.POST.get('category_id')
            name = request.POST.get('name')
            size = request.POST.get('size')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')       

            
            if not all([category_id ,name,size,price,stock,description,image_file]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            product_service.product_create(category_id ,name,size,price,stock,description,image_file)
            return JsonResponse({'message': 'product created successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminProductUpdateView(View):
    def get(self,request, product_id):
        product = product_service.get_product_by_id(product_id)
        categories = category_service.get_all_active_categories()
        return render(request,'admin/product/product_update.html',{'product':product,'categories':categories})
    
    def post(self, request, product_id):
        try:
            category_id = request.POST.get('category_id')
            name = request.POST.get('name')
            size = request.POST.get('size')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            image_file = request.FILES.get('image') 
                   
            if not all([category_id ,name,size,price,stock,description,image_file]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            product_service.product_update(product_id,category_id ,name,size,price,stock,description,image_file)
            return JsonResponse({'message': 'product created successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
      
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminProductToggleActiveView(View):
    def post(self, request):
        data = json.loads(request.body)
        is_active = data.get('is_active')
        product_id = data.get('product_id')
        product = product_service.toggle_active_product(product_id, is_active)
        return JsonResponse({
            'success': True,
            'product_id': product.id,
            'is_active': product.is_active
        })
    
class CategoryProductList(View):
    def get(self,request,category_id):
        products = product_service.get_products_by_category(category_id)
        return render(request, 'enduser/product_list.html',{'products':products})


class ProductDetailsView(View):
    def get(self,request, product_id):
        product = product_service.get_product_by_id(product_id)
        return render(request, 'enduser/product_details.html', {'product':product})