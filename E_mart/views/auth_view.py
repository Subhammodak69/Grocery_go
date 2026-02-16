from django.views import View
from django.http import JsonResponse
from E_mart.services import auth_service,user_service
from django.contrib.auth import login,logout
import json
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from E_mart.constants.decorators import anonymous_required

@method_decorator(csrf_exempt,name='dispatch')
@method_decorator(anonymous_required(redirect_url='home'), name='dispatch')
class LoginView(View):
    def get(self,request):
        return render(request, 'auth/login.html')
    
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        is_user = user_service.is_user_exist_by_email(email)
        if not is_user:
            return JsonResponse({'message': 'User not Found'})
        user = user_service.get_user_by_email(email)
        
        login(request, user)
        return JsonResponse({'message': 'Login Successfully'})

    
@method_decorator(csrf_exempt,name='dispatch')   
@method_decorator(anonymous_required(redirect_url='home'), name='dispatch') 
class SignupView(View):
    def get(self,request):
        return render(request, 'auth/signup.html')
    
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone')
        address = data.get('address')

        if not email or not first_name or not last_name or not phone_number:
            return JsonResponse({'message': 'Missing required fields'}, status=400)

        try:
            user = user_service.create_user(email, first_name, last_name, phone_number, address)
        except Exception as e:
            return JsonResponse({'message': f'User Not Created: {str(e)}'}, status=500)
        
        login(request, user)
        return JsonResponse({'message': 'Signup completed'}, status=201)


@method_decorator(csrf_exempt,name='dispatch')   
@method_decorator(anonymous_required(redirect_url='home'), name='dispatch')
class OtpSendView(View):
    def post(self,request):
        data = json.loads(request.body)
        purpose = data.get('purpose')
        email = data.get('email')
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        is_user = user_service.is_user_exist_by_email(email)
        if purpose == 'login':
            if is_user:
                otp = auth_service.generate_secure_otp()
                print(otp)
                try:
                    auth_service.send_otp_to_email(email,otp)
                except Exception:
                    return JsonResponse({'message': 'Cannot be send otp to the email!'})
                auth_service.save_otp(email,otp)
            else:
                return JsonResponse({'message': 'User does not exists'})
        else:
            if not is_user:
                otp = auth_service.generate_secure_otp()
                print("otp is:",otp)
                try:
                    auth_service.send_otp_to_email(email,otp)
                except Exception:
                    return JsonResponse({'message': 'Cannot be send otp to the email!'})
                auth_service.save_otp(email,otp)
            else:
                return JsonResponse({'message': 'User already exists'})
        return JsonResponse({'message': 'OTP sent successfully'})
    
    
@method_decorator(csrf_exempt,name='dispatch')   
@method_decorator(anonymous_required(redirect_url='home'), name='dispatch')
class VerifyOtpView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')
        if not email:
            return JsonResponse({ 'message': 'Email not found'})
        if not otp:
            return JsonResponse({'message': 'Otp not found'})
        res = auth_service.check_otp(email,otp)
        if res:
            return JsonResponse({ 'message':'verified'})
        return JsonResponse({'message': 'Incorrect otp'})
    
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
        
        
@method_decorator(csrf_exempt,name='dispatch') 
@method_decorator(anonymous_required(redirect_url='admin'), name='dispatch')         
class AdminLoginView(View):
    def get(self,request):
        return render(request, 'auth/admin_login.html')
    
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required.'}, status=400)

        user = user_service.check_admin_login(email, password)
        if user is None:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)

        if not user.is_staff:
            return JsonResponse({'error': 'User is not an admin.'}, status=403)
        
        login(request,user)

        return JsonResponse({'message': 'Login successful', 'email': user.email})