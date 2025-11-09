from E_mart.models import User
from django.contrib.auth.hashers import check_password

def get_all_users():
    return User.objects.filter(role=2).order_by('id')

def check_is_admin(user_id):
    user = User.objects.filter(id = user_id, is_active = True).first()
    if user.role == 1:
        return True
    return False

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

def update_user(user_id,email,first_name,last_name,phone_number,address):
    user = get_active_user_obj_by_id(user_id)
    user.email = email
    user.username = email
    user.first_name = first_name
    user.last_name = last_name
    user.phone_number = phone_number
    user.address = address
    user.save() 
    return user

def update_enduser(user_id,phone,main_address,optional_address):
    print(phone,main_address,optional_address)
    user = User.objects.get(id=user_id, is_active = True)
    user.phone_number = phone
    user.address = main_address
    user.optional_address = optional_address
    user.save() 
    print(user)
    return
   
   
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

def get_user_data_by_id(user_id):
    user = User.objects.filter(id = user_id, is_active = True).first()
    user_data = {
        'full_name': f"{user.first_name} {user.last_name}",
        'optional_address':user.optional_address if user.optional_address else ''
    }
    return user_data