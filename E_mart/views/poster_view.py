from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import admin_required
from E_mart.services import poster_service,product_service,category_service
import json


@method_decorator(admin_required, name='dispatch')
class AdminPosterListView(View):
    def get(self,request):
        posters = poster_service.get_all_posters()
        return render(request,'admin/poster/poster_list.html',{'posters':posters})
    
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterCreateView(View):
    def get(self,request):
        products = product_service.get_all_active_products()
        return render(request,'admin/poster/poster_create.html',{'products':products})
    
    def post(self, request):
        try:
            product_id = request.POST.get('product_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')  
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            if not all([product_id,title, image_file, start_date, end_date]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            poster_service.poster_create(product_id,title, description, image_file, start_date, end_date)
            return JsonResponse({'message': 'Poster created successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterUpdateView(View):
    def get(self,request, poster_id):
        poster = poster_service.get_poster_by_id(poster_id)
        products = product_service.get_all_active_products()
        return render(request,'admin/poster/poster_update.html',{'poster':poster,'products':products})
    
    def post(self, request, poster_id):
        try:
            product_id = request.POST.get('product_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

           
            if not all([product_id,title,description,start_date, end_date]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            poster_service.poster_update(poster_id,product_id,title, description, image_file, start_date, end_date)
            return JsonResponse({'message': 'Poster created successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
      
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterToggleActiveView(View):
    def post(self, request):
        data = json.loads(request.body)
        is_active = data.get('is_active')
        poster_id = data.get('poster_id')
        poster = poster_service.toggle_active_poster(poster_id, is_active)
        return JsonResponse({
            'success': True,
            'poster_id': poster.id,
            'is_active': poster.is_active
        })