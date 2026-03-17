# views/admin_views.py
from django.views import View
from django.shortcuts import render
from E_mart.constants.decorators import admin_required, delivery_worker_required
from django.utils.decorators import method_decorator
from E_mart.services import worker_service, deliveryperson_service, delivery_service
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

@method_decorator(admin_required, name='dispatch')
class AdminWorkerManagementView(View):
    """Single page for all worker management operations"""
    
    def get(self, request):
        workers_data = worker_service.get_all_workers()
        return render(request, 'admin/worker/worker_list.html', {'workers': workers_data})

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminWorkerToggleActiveView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            is_active = data.get('is_active')
            worker_id = data.get('worker_id')
            worker = worker_service.toggle_active_worker(worker_id, is_active)
            return JsonResponse({
                'success': True,
                'worker_id': worker.id,
                'is_active': worker.is_active
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminWorkerCreateAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'{field} is required.'}, status=400)
            
            # Check if worker already exists
            from E_mart.models import User
            if User.objects.filter(email=data.get('email')).exists():
                return JsonResponse({'error': 'Worker with this email already exists.'}, status=400)
            
            # Create worker
            user = User.objects.create(
                username=data.get('email'),
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                phone_number=data.get('phone_number'),
                password=make_password(data.get('password')),
                role=3,  # Worker role
                is_active=True
            )
            
            # Create delivery person record
            deliveryperson_service.create_deliveryperson(user)
            
            return JsonResponse({
                'success': True,
                'message': 'Worker created successfully.',
                'worker': {
                    'id': user.id,
                    'full_name': user.get_full_name(),
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'is_active': user.is_active,
                    'role': user.role
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminWorkerUpdateAPIView(View):
    def post(self, request, worker_id):
        try:
            data = json.loads(request.body)
            
            # Get worker
            from E_mart.models import User
            try:
                worker = User.objects.get(id=worker_id, role=3)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Worker not found.'}, status=404)
            
            # Update fields
            if data.get('first_name'):
                worker.first_name = data.get('first_name')
            if data.get('last_name'):
                worker.last_name = data.get('last_name')
            if data.get('email'):
                # Check if email is taken by another worker
                if User.objects.filter(email=data.get('email')).exclude(id=worker_id).exists():
                    return JsonResponse({'error': 'Email already in use by another worker.'}, status=400)
                worker.email = data.get('email')
                worker.username = data.get('email')
            if data.get('phone_number'):
                worker.phone_number = data.get('phone_number')
            if data.get('password'):
                worker.password = make_password(data.get('password'))
            
            worker.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Worker updated successfully.',
                'worker': {
                    'id': worker.id,
                    'full_name': worker.get_full_name(),
                    'email': worker.email,
                    'phone_number': worker.phone_number,
                    'is_active': worker.is_active,
                    'role': worker.role
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
class AdminWorkerDetailAPIView(View):
    def get(self, request, worker_id):
        try:
            from E_mart.models import User
            worker = User.objects.get(id=worker_id, role=3)
            
            # Get delivery person details if exists
            from E_mart.models import DeliveryPerson
            try:
                delivery_person = DeliveryPerson.objects.get(user=worker)
                is_available = delivery_person.is_available
                amount = str(delivery_person.amount) if delivery_person.amount else '0'
            except DeliveryPerson.DoesNotExist:
                is_available = False
                amount = '0'
            
            data = {
                'id': worker.id,
                'username': worker.username,
                'full_name': worker.get_full_name(),
                'first_name': worker.first_name,
                'last_name': worker.last_name,
                'email': worker.email,
                'phone_number': worker.phone_number,
                'role': worker.role,
                'role_display': 'Delivery Worker',
                'is_active': worker.is_active,
                'is_available': is_available,
                'amount': amount,
                'date_joined': worker.date_joined.strftime('%B %d, %Y') if worker.date_joined else None,
                'last_login': worker.last_login.strftime('%B %d, %Y %H:%M') if worker.last_login else None,
            }
            return JsonResponse(data)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Worker not found'}, status=404)

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

