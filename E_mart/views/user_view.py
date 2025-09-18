from django.views import View
from django.shortcuts import render
from E_mart.constants.decorators import admin_required
from django.utils.decorators import method_decorator
from E_mart.services import user_service
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

method_decorator(admin_required,name='dispatch')
class AdminUserListView(View):
    def get(self,request):
        users_data = user_service.get_all_users()
        return render(request,'admin/user/user_list.html',{'users':users_data})
    
    
@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminUserToggleActiveView(View):
    def post(self, request):
        print("hello")
        data = json.loads(request.body)
        is_active = data.get('is_active')
        user_id = data.get('user_id')
        print("going",user_id,is_active)
        user = user_service.toggle_active_user(user_id, is_active)
        print("user=>",user.is_active)
        return JsonResponse({
            'success': True,
            'user_id': user.id,
            'is_active': user.is_active
        })

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminUserCreateView(View):

    def get(self, request):
        return render(request, 'admin/user/user_create.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)  # For debugging

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            address = data.get('address')

            # Validate required fields
            if not all([first_name, last_name, email, phone_number, address]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            # Call your user_service to create user (implement this accordingly)
            user_service.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                address=address
            )

            return JsonResponse({'message': 'User created successfully.'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            # Log the error in production
            return JsonResponse({'error': str(e)}, status=500)
    