from django.views import View
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import admin_required
from E_mart.services import product_service,category_service,review_service,order_service
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
            original_price = request.POST.get('original_price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')       

            
            if not all([category_id ,name,size,price,original_price,stock,description,image_file]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            product_service.product_create(category_id ,name,size,price,original_price,stock,description,image_file)
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
            original_price = request.POST.get('original_price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            image_file = request.FILES.get('image',None) 
                   
            if not all([category_id ,name,size,price,original_price,stock,description]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            product_service.product_update(product_id,category_id ,name,size,price,original_price,stock,description,image_file)
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
        category = category_service.get_category_by_id(category_id)
        products = product_service.get_products_by_category(category_id)
        return render(request, 'enduser/product_list.html',{'products':products,'category':category})


class ProductDetailsView(View):
    def get(self,request, product_id):
        order_service.free_garbage_order()
        product = product_service.get_product_by_id(product_id)
        review_data = review_service.get_product_review_data(product.id)
        rating = review_service.get_rating_by_product_id(product_id)
        discount = product_service.get_product_offer_by_id(product.id)
        return render(
            request, 
            'enduser/product_details.html', 
                {
                    'product':product,
                    'discount':discount,
                    'reviews':review_data,
                    'review_len':len(review_data),
                    'rating':rating
                })

class ProductSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse([], safe=False)  # Return empty list if no query

        # Search products by name or brand case-insensitively
        
        products = product_service.get_searched_product_data(query)

        # Prepare JSON response data
        results = [
            {
                'product_name': product.name,
                'category_name': product.category.name,
                'product_id': product.id,
                'category_id':product.category.id
            }
            for product in products
        ]
        return JsonResponse(results, safe=False)