from django.views import View
from django.shortcuts import render
from E_mart.constants.decorators import admin_required
from django.utils.decorators import method_decorator

method_decorator(admin_required,name='dispatch')
class AdminUserListView(View):
    def get(self,request):
        return render(request,'admin/user/user_list.html')