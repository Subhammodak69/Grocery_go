from E_mart.models import User

def create_user(email,first_name,last_name,phone_number,address):
    return User.objects.create(
        username = email,
        email = email,
        first_name = first_name,
        last_name = last_name,
        phone_number = phone_number,
        address = address,
        role = 3
    ) 