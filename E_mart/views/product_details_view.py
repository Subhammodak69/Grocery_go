import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from E_mart.constants.decorators import admin_required  # Adjust import as needed
from E_mart.services import product_details_service, product_service  # Adjust service imports


@method_decorator(admin_required, name='dispatch')
class AdminProductDetailsListView(View):
    def get(self, request):
        product_details = product_details_service.get_all_product_details()
        return render(request, 'admin/product_details/productdetails_list.html', {'product_details': product_details})


@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminProductDetailsCreateView(View):
    def get(self, request):
        products = product_service.get_all_products()
        return render(request, 'admin/product_details/productdetails_create.html', {'products': products})

    def post(self, request):
        try:
            # Get data from POST parameters (not JSON body)
            product_id = request.POST.get('product')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            size = request.POST.get('size')
            image_file = request.FILES.get('image')
            is_active = request.POST.get('is_active') == 'true'

            print(product_id, price, stock, size, image_file, is_active)
            
            if not all([product_id, price, stock, size, image_file]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            product_details_service.product_details_create(
                product_id=product_id,
                price=price,
                stock=stock,
                size=size,
                image_file=image_file,
                is_active=is_active
            )
            return JsonResponse({'message': 'Product details created successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminProductDetailsUpdateView(View):
    def get(self, request, product_details_id):
        product_detail = product_details_service.get_product_details_by_id(product_details_id)
        products = product_service.get_all_products()
        return render(request,
                      'admin/product_details/productdetails_update.html',
                      {'product_details': product_detail, 'products': products})

    def post(self, request, product_details_id):
        try:
            product_id = request.POST.get('product')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            size = request.POST.get('size')
            image_file = request.FILES.get('image')  # This will be None if no file uploaded
            
            # ✅ Improved boolean handling
            is_active_value = request.POST.get('is_active', 'false').lower()
            is_active = is_active_value in ['true', 'on', '1']

            # Validate required fields
            if not all([product_id, price, stock, size]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # ✅ Pass image_file even if None - let the service handle it
            product_details_service.product_details_update(
                product_details_id=product_details_id,
                product_id=product_id,
                price=price,
                stock=stock,
                size=size,
                image_file=image_file,  # Can be None for no image update
                is_active=is_active
            )
            return JsonResponse({'message': 'Product details updated successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminProductDetailsToggleActiveView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            is_active = data.get('is_active')
            product_details_id = data.get('product_details_id')
            product_detail = product_details_service.toggle_active_product(product_details_id,is_active)
            return JsonResponse({
                'success': True,
                'product_details_id': product_detail.id,
                'is_active': product_detail.is_active
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
