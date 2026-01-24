from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import admin_required,delivery_worker_required,homeNavigate
from E_mart.services import poster_service,category_service,product_service,delivery_service,order_service,exchange_or_return_service
import json
from django.http import JsonResponse

@method_decorator(homeNavigate, name='dispatch')
class HomeView(View):
    def get(self,request):  
        categories = category_service.get_all_active_categories()
        posters = poster_service.get_all_showable_posters()
        products = product_service.get_all_active_products()
        return render(request,'enduser/home.html',{'posters':posters,'categories':categories, 'products':products})
    
@method_decorator(admin_required, name='dispatch')
class AdminHomeView(View):
    def get(self,request):
        return render(request,'admin/home.html')

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

