from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from E_mart.constants.decorators import delivery_worker_required,admin_required
from E_mart.services import delivery_service,order_service,deliveryperson_service
from django.http import JsonResponse
import json


@method_decorator(delivery_worker_required,name='dispatch')
class DeliveriesListView(View):
    def get(self, request):
        worker = delivery_service.get_delivery_worker_obj_by_user_id(request.user)
        deliveries = delivery_service.get_deliveries_by_deliveryPerson(worker)
        return render(request, 'delivery/deliveries.html',{'deliveries':deliveries})
    
@method_decorator(delivery_worker_required,name='dispatch')
class PickUpsListView(View):
    def get(self, request):
        worker = delivery_service.get_delivery_worker_obj_by_user_id(request.user)
        pickups = delivery_service.get_pickups_by_deliveryPerson(worker)
        return render(request, 'delivery/pickups.html',{'pickups':pickups})
    


#admin

@method_decorator(admin_required, name='dispatch')
class AdminDeliveryOrPickupListView(View):
    def get(self, request):
        deliveries = delivery_service.get_all_deliveries() 
        return render(request, 'admin/delivery_or_pickup/delivery_pickup_list.html', {'deliveries': deliveries})

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminDeliveryOrPickupCreateView(View):
    def get(self, request):
        orders = order_service.get_all_orders()
        delivery_persons = deliveryperson_service.get_available_delivery_boys()
        return render(request, 'admin/delivery_or_pickup/delivery_pickup_create.html', {
            'orders': orders, 
            'delivery_persons': delivery_persons
        })
    
    def post(self, request):
        try:
            order_id = request.POST.get('order')
            address = request.POST.get('address')
            delivery_person_id = request.POST.get('delivery_person')
            status = request.POST.get('status')
            purpose = request.POST.get('purpose')
            delivered_at = request.POST.get('delivered_at')
            is_active = request.POST.get('is_active', 'true').lower() == 'true'

            if not all([order_id, address, status, purpose]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            delivery_service.delivery_create(
                order_id, address, delivery_person_id, status, 
                purpose, delivered_at, is_active
            )
            return JsonResponse({'message': 'Delivery/Pickup created successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminDeliveryOrPickupUpdateView(View):
    def get(self, request, delivery_id):
        delivery = delivery_service.get_delivery_by_id(delivery_id)
        orders = order_service.get_all_orders()
        delivery_persons = deliveryperson_service.get_available_delivery_boys()
        return render(request, 'admin/delivery_or_pickup/delivery_pickup_update.html', {
            'delivery': delivery, 
            'orders': orders, 
            'delivery_persons': delivery_persons
        })
    
    def post(self, request, delivery_id):
        try:
            order_id = request.POST.get('order')
            address = request.POST.get('address')
            delivery_person_id = request.POST.get('delivery_person')
            status = request.POST.get('status')
            purpose = request.POST.get('purpose')
            delivered_at = request.POST.get('delivered_at')
            is_active = request.POST.get('is_active', 'true').lower() == 'true'

            delivery_service.delivery_update(
                delivery_id, order_id, address, delivery_person_id, 
                status, purpose, delivered_at, is_active
            )
            return JsonResponse({'message': 'Delivery/Pickup updated successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminDeliveryOrPickupToggleActiveView(View):
    def post(self, request):
        data = json.loads(request.body)
        is_active = data.get('is_active')
        delivery_id = data.get('delivery_id')
        delivery = delivery_service.toggle_active_delivery(delivery_id, is_active)
        return JsonResponse({
            'success': True,
            'delivery_id': delivery.id,
            'is_active': delivery.is_active
        })
