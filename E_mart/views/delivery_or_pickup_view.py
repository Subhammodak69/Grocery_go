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
    

@method_decorator(admin_required, name='dispatch')
class AdminDeliveryOrPickupListView(View):
    def get(self, request):
        deliveries = delivery_service.get_all_deliveries()
        orders = order_service.get_all_orders()
        delivery_persons = deliveryperson_service.get_available_delivery_boys()
        return render(request, 'admin/delivery_pickup_list.html', {
            'deliveries': deliveries,
            'orders': orders,
            'delivery_persons': delivery_persons
        })

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminDeliveryOrPickupCreateView(View):
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

            delivery = delivery_service.delivery_create(
                order_id, address, delivery_person_id, status, 
                purpose, delivered_at, is_active
            )
            
            # Return the created delivery data for dynamic UI update
            return JsonResponse({
                'success': True,
                'message': 'Delivery/Pickup created successfully!',
                'delivery': {
                    'id': delivery.id,
                    'order_id': delivery.order.id,
                    'address': delivery.address,
                    'purpose': purpose,
                    'status': status,
                    'delivery_person_name': delivery.delivery_person.user.get_full_name() if delivery.delivery_person and delivery.delivery_person.user else 'Unassigned',
                    'is_active': delivery.is_active,
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminDeliveryOrPickupDetailView(View):
    def get(self, request, delivery_id):
        try:
            delivery = delivery_service.get_delivery_by_id(delivery_id)
            if not delivery:
                return JsonResponse({'error': 'Delivery not found'}, status=404)
            
            # Get all orders for dropdown
            orders = order_service.get_all_orders()
            orders_list = []
            for order in orders:
                orders_list.append({
                    'id': order.id,
                    'display': f"Order #{order.id} - {order.user.get_full_name() or order.user.username}"
                })
            
            # Get all delivery persons for dropdown
            delivery_persons = deliveryperson_service.get_available_delivery_boys()
            delivery_persons_list = []
            for person in delivery_persons:
                delivery_persons_list.append({
                    'id': person.id,
                    'display': person.user.get_full_name() or person.user.username
                })
            
            # Prepare delivery data
            delivery_data = {
                'id': delivery.id,
                'order_id': delivery.order.id,
                'address': delivery.address,
                'purpose': delivery.purpose,
                'purpose_display': delivery.get_purpose_display() if hasattr(delivery, 'get_purpose_display') else str(delivery.purpose),
                'status': delivery.status,
                'status_display': delivery.get_status_display() if hasattr(delivery, 'get_status_display') else str(delivery.status),
                'is_active': delivery.is_active,
                'created_at': delivery.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(delivery, 'created_at') and delivery.created_at else None,
                'delivered_at': delivery.delivered_at.strftime('%Y-%m-%d %H:%M:%S') if delivery.delivered_at else None,
                'delivery_person': {
                    'id': delivery.delivery_person.id if delivery.delivery_person else None,
                    'name': delivery.delivery_person.user.get_full_name() if delivery.delivery_person and delivery.delivery_person.user else None,
                    'phone': delivery.delivery_person.user.phone_number if delivery.delivery_person and delivery.delivery_person.user else None
                } if delivery.delivery_person else None,
                'order_details': {
                    'user_name': delivery.order.user.get_full_name() or delivery.order.user.username,
                    'user_phone': delivery.order.user.phone_number,
                    'total_price': str(delivery.order.total_price),
                    'items_count': delivery.order.order_items.count()
                },
                'orders_list': orders_list,
                'delivery_persons_list': delivery_persons_list
            }
            return JsonResponse(delivery_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminDeliveryOrPickupUpdateView(View):
    def post(self, request, delivery_id):
        try:
            order_id = request.POST.get('order')
            address = request.POST.get('address')
            delivery_person_id = request.POST.get('delivery_person')
            status = request.POST.get('status')
            purpose = request.POST.get('purpose')
            delivered_at = request.POST.get('delivered_at')
            is_active = request.POST.get('is_active', 'true').lower() == 'true'

            delivery = delivery_service.delivery_update(
                delivery_id, order_id, address, delivery_person_id, 
                status, purpose, delivered_at, is_active
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Delivery/Pickup updated successfully!',
                'delivery': {
                    'id': delivery.id,
                    'order_id': delivery.order.id,
                    'address': delivery.address,
                    'purpose': purpose,
                    'status': status,
                    'delivery_person_name': delivery.delivery_person.user.get_full_name() if delivery.delivery_person and delivery.delivery_person.user else 'Unassigned',
                    'is_active': delivery.is_active,
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminDeliveryOrPickupToggleActiveView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            is_active = data.get('is_active')
            delivery_id = data.get('delivery_id')
            delivery = delivery_service.toggle_active_delivery(delivery_id, is_active)
            return JsonResponse({
                'success': True,
                'delivery_id': delivery.id,
                'is_active': delivery.is_active
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)