from django.views import View
from django.shortcuts import render

class HomeView(View):
    def get(self,request):
        print(request.user)
        return render(request,'enduser/home.html')
    