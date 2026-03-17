from django.views import View
from django.shortcuts import render
from E_mart.constants.decorators import admin_required,enduser_required
from django.utils.decorators import method_decorator
from E_mart.services import user_service
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from E_mart.models import User

@method_decorator(admin_required, name='dispatch')
class AdminUserManagementView(View):
    """Single page for all user management operations"""
    
    def get(self, request):
        users_data = user_service.get_all_users()
        return render(request, 'admin/user_list.html', {'users': users_data})

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminUserToggleActiveView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            is_active = data.get('is_active')
            user_id = data.get('user_id')
            user = user_service.toggle_active_user(user_id, is_active)
            return JsonResponse({
                'success': True,
                'user_id': user.id,
                'is_active': user.is_active
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminUserCreateAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'password']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'{field} is required.'}, status=400)
            
            # Check if user already exists
            if User.objects.filter(email=data.get('email')).exists():
                return JsonResponse({'error': 'User with this email already exists.'}, status=400)
            
            # Create user
            user = User.objects.create(
                username=data.get('email'),  # Use email as username
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                phone_number=data.get('phone_number'),
                address=data.get('address'),
                optional_address=data.get('optional_address', ''),
                password=make_password(data.get('password')),
                role=2,  # Customer role
                is_active=True
            )
            
            return JsonResponse({
                'success': True,
                'message': 'User created successfully.',
                'user': {
                    'id': user.id,
                    'full_name': user.get_full_name(),
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'address': user.address,
                    'optional_address': user.optional_address,
                    'is_active': user.is_active,
                    'role': user.role
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AdminUserUpdateAPIView(View):
    def post(self, request, user_id):
        try:
            data = json.loads(request.body)
            
            # Get user
            try:
                user = User.objects.get(id=user_id, role=2)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found.'}, status=404)
            
            # Update fields
            if data.get('first_name'):
                user.first_name = data.get('first_name')
            if data.get('last_name'):
                user.last_name = data.get('last_name')
            if data.get('email'):
                # Check if email is taken by another user
                if User.objects.filter(email=data.get('email')).exclude(id=user_id).exists():
                    return JsonResponse({'error': 'Email already in use by another user.'}, status=400)
                user.email = data.get('email')
                user.username = data.get('email')  # Keep username in sync
            if data.get('phone_number'):
                user.phone_number = data.get('phone_number')
            if data.get('address'):
                user.address = data.get('address')
            if data.get('optional_address') is not None:
                user.optional_address = data.get('optional_address')
            if data.get('password'):
                user.password = make_password(data.get('password'))
            
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'User updated successfully.',
                'user': {
                    'id': user.id,
                    'full_name': user.get_full_name(),
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'address': user.address,
                    'optional_address': user.optional_address,
                    'is_active': user.is_active,
                    'role': user.role
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(admin_required, name='dispatch')
class AdminUserDetailAPIView(View):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, role=2)
            
            # Get role display
            role_display = 'Admin' if user.role == 1 else 'Customer' if user.role == 2 else 'Worker'
            
            data = {
                'id': user.id,
                'username': user.username,
                'full_name': user.get_full_name(),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'address': user.address,
                'optional_address': user.optional_address,
                'role': user.role,
                'role_display': role_display,
                'is_active': user.is_active,
                'date_joined': user.date_joined.strftime('%B %d, %Y') if user.date_joined else None,
                'last_login': user.last_login.strftime('%B %d, %Y %H:%M') if user.last_login else None,
            }
            return JsonResponse(data)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

@method_decorator(enduser_required, name='dispatch')
class UserProfileView(View):
    def get(self,request):
        user_data = user_service.get_user_data_by_id(request.user.id)
        user = request.user
        return render(request, 'enduser/profile.html',{'user':user,'user_data':user_data})


@method_decorator(enduser_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UserProfileUpdateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            phone = data.get('phone')
            main_address = data.get('mainAddress')
            optional_address = data.get('optionalAddress')

            user_service.update_enduser(request.user.id,phone,main_address,optional_address)
            return JsonResponse({'success': True, 'message': 'Profile updated successfully.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
