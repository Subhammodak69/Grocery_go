from E_mart.models import User

def get_all_users():
    return User.objects.all()

def get_user(user_id):
    return User.objects.get(id = user_id, is_active = True)

def get_user_by_email(email):
    return User.objects.get(email = email, is_active = True)

def is_user_exist_by_email(email):
    return User.objects.filter(email=email, is_active = True).exists()

def create_user(email,first_name,last_name,phone_number,address):
    return User.objects.create(
        email = email,
        first_name = first_name,
        last_name = last_name,
        phone_number = phone_number,
        address = address
    )