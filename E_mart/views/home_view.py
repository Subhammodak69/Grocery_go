from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required,admin_required

@method_decorator(enduser_required, name='dispatch')
class HomeView(View):
    def get(self,request):
        print(request.user)
        return render(request,'enduser/home.html')
    
@method_decorator(admin_required, name='dispatch')
class AdminHomeView(View):
    def get(self,request):
        return render(request,'admin/home.html')