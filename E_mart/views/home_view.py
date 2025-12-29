from django.views import View
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required,admin_required,delivery_worker_required,homeNavigate
from E_mart.services import poster_service,category_service,product_service,delivery_service
import json

@method_decorator(homeNavigate, name='dispatch')
class HomeView(View):
    def get(self,request):  
        print(request.session.get('payment_data'))       
        categories = category_service.get_all_active_categories()
        posters = poster_service.get_all_showable_posters()
        products = product_service.get_all_active_products()
        return render(request,'enduser/home.html',{'posters':posters,'categories':categories, 'products':products})
    
@method_decorator(admin_required, name='dispatch')
class AdminHomeView(View):
    def get(self,request):
        return render(request,'admin/home.html')

@method_decorator(delivery_worker_required, name='dispatch')
class DeliveryWorkerHomeView(View):
    def get(self, request):
        user = request.user
        worker = delivery_service.get_delivery_worker_obj_by_user_id(user)
        stats = delivery_service.get_last_7_days_stats(worker)
        print(stats)

        data = {
            "labels": stats["labels"],
            "deliveries": stats["deliveries"],
            "pickups": stats["pickups"],
        }

        context = {
            "total_deliveries": stats["total_deliveries"],
            "total_pickups": stats["total_pickups"],
            "completion_rate": stats["completion_rate"],
            "chart_data": json.dumps(data),
        }

        return render(request, "delivery/home.html", context)
