from django.views import View
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import admin_required,delivery_worker_required,homeNavigate
from E_mart.services import poster_service,category_service,product_service,delivery_service,order_service,exchange_or_return_service,admin_dashboard_service
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from E_mart.constants.default_values import OrderStatus

@method_decorator(homeNavigate, name='dispatch')
class HomeView(View):
    def get(self,request):  
        categories = category_service.get_all_active_categories()
        posters = poster_service.get_all_showable_posters()
        products = product_service.get_all_active_products()
        return render(request,'enduser/home.html',{'posters':posters,'categories':categories, 'products':products})
    
@method_decorator(admin_required, name='dispatch')
class AdminHomeView(View):
    def get(self, request):
        context = admin_dashboard_service.get_all_dashboard_data()
        return render(request, 'admin/dashboard.html', context)
    
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminOrderDetailView(View):
    def get(self, request, order_id):
        context = admin_dashboard_service.get_order_data(order_id)
        return render(request, 'admin/order/order_details.html', context)

    def post(self, request, order_id):

        action = request.POST.get('action')

        if action == 'update_status':
            new_status = request.POST.get('status')

            if new_status:
                old_status, updated_status = admin_dashboard_service.update_order_status(order_id, new_status)

                messages.success(
                    request,
                    f'Order #{order_id} status updated from {OrderStatus(old_status).name} to {OrderStatus(updated_status).name}'
                )

        elif action == 'assign_delivery':
            person_id = request.POST.get('delivery_person')

            if person_id:
                admin_dashboard_service.assign_delivery_person(order_id, person_id)
                messages.success(request, f'Delivery person assigned successfully to Order #{order_id}')

        elif action == 'update_payment':
            payment_id = request.POST.get('payment_id')
            new_status = request.POST.get('payment_status')

            if payment_id and new_status:
                admin_dashboard_service.update_payment_status(payment_id, new_status)
                messages.success(request, f'Payment status updated for Order #{order_id}')

        elif action == 'cancel_order':
            admin_dashboard_service.cancel_order(order_id)
            messages.success(request, f'Order #{order_id} has been cancelled')

        return redirect('admin_order_detail', order_id=order_id)

@method_decorator(admin_required, name='dispatch')
class AdminNotificationsView(View):
    def get(self, request):
        unassigned_orders = order_service.get_all_unassigned_orders()
        
        unassigned_pickups = exchange_or_return_service.get_all_unassigned_exchanges() 
        
        return JsonResponse({
            'unassigned_orders_count': unassigned_orders.count(),
            'unassigned_pickups_count': unassigned_pickups.count()
        })

@method_decorator(delivery_worker_required, name='dispatch')
class DeliveryWorkerHomeView(View):
    def get(self, request):
        user = request.user
        worker = delivery_service.get_delivery_worker_obj_by_user_id(user)
        stats = delivery_service.get_last_7_days_stats(worker)
        complete_delivery_or_pickup_count = len(delivery_service.get_total_delivery_or_pickup_by_worker(worker)) 
        total_services_count = len(delivery_service.get_all_delivery_pickups_of_worker(worker))
        pending_count = (total_services_count)-(complete_delivery_or_pickup_count)
        data = {
            "labels": stats["labels"],
            "deliveries": stats["deliveries"],
            "pickups": stats["pickups"],
            "pendings":pending_count,
        }

        context = {
            "total_deliveries": stats["total_deliveries"],
            "total_pickups": stats["total_pickups"],
            "completion_rate": stats["completion_rate"],
            "chart_data": json.dumps(data),
        }

        return render(request, "delivery/home.html", context)
    
@method_decorator(delivery_worker_required, name='dispatch')

class DeliveryOrPickupNotifications(View):
    def get(self,request):
        delivery_count = delivery_service.get_delivery_count_by_worker(request.user)
        pickup_count = delivery_service.get_pickup_count_by_worker(request.user)
        return JsonResponse({
            'pending_deliveries_count': delivery_count,
            'pending_pickups_count': pickup_count
        })