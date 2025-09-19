from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import admin_required
from E_mart.services import poster_service
import json


@method_decorator(admin_required, name='dispatch')
class AdminPosterListView(View):
    def get(self,request):
        posters = poster_service.get_all_posters()
        print(posters)
        return render(request,'admin/poster/poster_list.html',{'posters':posters})
    
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterCreateView(View):
    def get(self,request):
        return render(request,'admin/poster/poster_create.html')
    
    def post(self, request):
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')  
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            
            if not all([title, image_file, start_date, end_date]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            poster_service.poster_create(title, description, image_file, start_date, end_date)
            return JsonResponse({'message': 'Poster created successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterUpdateView(View):
    def get(self,request, poster_id):
        poster = poster_service.get_poster_by_id(poster_id)
        return render(request,'admin/poster/poster_update.html',{'poster':poster})
    
    def post(self, request, poster_id):
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            image_file = request.FILES.get('image')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

           
            if not all([title,description,start_date, end_date]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            poster_service.poster_update(poster_id,title, description, image_file, start_date, end_date)
            return JsonResponse({'message': 'Poster created successfully!'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
      
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPosterToggleActiveView(View):
    def post(self, request):
        print("hello")
        data = json.loads(request.body)
        is_active = data.get('is_active')
        poster_id = data.get('poster_id')
        print("going",poster_id,is_active)
        poster = poster_service.toggle_active_poster(poster_id, is_active)
        print("poster=>",poster.is_active)
        return JsonResponse({
            'success': True,
            'poster_id': poster.id,
            'is_active': poster.is_active
        })