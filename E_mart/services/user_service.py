from E_mart.models import User
from django.contrib.auth.hashers import check_password

def get_all_users():
    return User.objects.filter(role=2).order_by('id')

def get_active_user_obj_by_id(user_id):
    return User.objects.filter(id=user_id,is_active=True).first()

def get_user_by_email(email):
    return User.objects.get(email = email, is_active = True)

def is_user_exist_by_email(email):
    return User.objects.filter(email=email, is_active = True).exists()

def create_user(email,first_name,last_name,phone_number,address):
    return User.objects.create(
        username = email,
        email = email,
        first_name = first_name,
        last_name = last_name,
        phone_number = phone_number,
        address = address
    )
   

    
   
   
#admin
    
def check_admin_login(email, password):
    try:
        user = User.objects.get(email=email, is_active=True, role=1)
    except User.DoesNotExist:
        return None

    if check_password(password, user.password):
        return user
    return None

def toggle_active_user(user_id,is_active):
    user = get_user_for_admin_by_id(user_id)
    user.is_active = is_active
    user.save()        
    return user

def get_user_for_admin_by_id(user_id):
    return User.objects.get(id = user_id)