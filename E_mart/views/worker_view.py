from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
import json
from E_mart.services import worker_service
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class AdminWorkerCreateView(View):
    def get(self,request):
        return render(request, 'admin/worker/worker_create.html')
    
    def post(self, request):
        try:
            data = json.loads(request.body)

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            address = data.get('address')

            # Validate required fields
            if not all([first_name, last_name, email, phone_number, address]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            # Call your user_service to create user (implement this accordingly)
            worker_service.create_user(
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
    
