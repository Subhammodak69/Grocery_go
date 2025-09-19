from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required,admin_required
from E_mart.services import poster_service

@method_decorator(enduser_required, name='dispatch')
class HomeView(View):
    def get(self,request):
        print(request.user)
        posters = poster_service.get_all_showable_posters()
        return render(request,'enduser/home.html',{'posters':posters})
    
@method_decorator(admin_required, name='dispatch')
class AdminHomeView(View):
    def get(self,request):
        return render(request,'admin/home.html')