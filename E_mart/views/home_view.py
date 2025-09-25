from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required,admin_required,delivery_worker_required
from E_mart.services import poster_service,category_service,product_service

# @method_decorator(enduser_required, name='dispatch')
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

@method_decorator(delivery_worker_required, name='dispatch')
class DeliveryWorkerHomeView(View):
    def get(self,request):
        return render(request,'delivery/base.html')