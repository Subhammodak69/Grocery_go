from django.views import View
from django.shortcuts import render
from E_mart.constants.decorators import admin_required,delivery_worker_required
from django.utils.decorators import method_decorator
from E_mart.services import worker_service,deliveryperson_service,delivery_service
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@method_decorator(admin_required, name='dispatch')
class AdminWorkerListView(View):
    def get(self,request):
        workers_data = worker_service.get_all_workers()
        return render(request,'admin/worker/worker_list.html',{'workers':workers_data})
    
    
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminworkerToggleActiveView(View):
    def post(self, request):
        data = json.loads(request.body)
        is_active = data.get('is_active')
        worker_id = data.get('worker_id')
        worker = worker_service.toggle_active_worker(worker_id, is_active) 
        return JsonResponse({
            'success': True,
            'worker_id': worker.id,
            'is_active': worker.is_active
        })
    

@method_decorator(csrf_exempt, name='dispatch')
class AdminWorkerCreateView(View):
    def get(self,request):
        return render(request, 'admin/worker/worker_create.html')
    
    def post(self, request):
        try:
            data = json.loads(request.body)

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone_number = data.get('phone_number')

            # Validate required fields
            if not all([first_name, last_name, email, phone_number]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            # Call your worker_service to create worker (implement this accordingly)
            user = worker_service.create_worker(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )
            if user:
                deliveryperson_service.create_deliveryperson(user)

            return JsonResponse({'message': 'worker created successfully.'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            # Log the error in production
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminWorkerUpdateView(View):

    def get(self, request,worker_id):
        worker = worker_service.get_worker_obj_by_id(worker_id) 
        return render(request, 'admin/worker/worker_update.html',{'worker':worker})

    def post(self, request,worker_id):
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone_number = data.get('phone_number')

            # Validate required fields
            if not all([first_name, last_name, email, phone_number]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            # Call your worker_service to create worker (implement this accordingly)
            worker_service.update_worker(
                worker_id=worker_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            ) 

            return JsonResponse({'message': 'worker Updated successfully.'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            # Log the error in production
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(delivery_worker_required, name='dispatch')
class DeliveryWorkerProfileView(View):
    def get(self,request):
        worker = worker_service.get_worker_by_user_obj(request.user)
        total_delivery_count = len(delivery_service.get_total_complete_deliveries_of_worker(worker))
        total_pickup_count = len(delivery_service.get_total_complete_pickups_of_worker(worker))
        complete_delivery_or_pickup_count = len(delivery_service.get_total_delivery_or_pickup_by_worker(worker)) 
        total_services_count = len(delivery_service.get_all_delivery_pickups_of_worker(worker))
        pending_count = (total_services_count)-(complete_delivery_or_pickup_count)
        data = {
            'deliveries_count':total_delivery_count,
            'pickups_count':total_pickup_count,
            'complete_count':complete_delivery_or_pickup_count,
            'pending_count':pending_count
        }
        return render(request,'delivery/profile.html',{'delivery_person':worker,'data':data})

