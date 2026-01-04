from E_mart.models import User,DeliveryPerson
from E_mart.constants.default_values import Role

def create_user(email,first_name,last_name,phone_number,address):
    return User.objects.create(
        username = email,
        email = email,
        first_name = first_name,
        last_name = last_name,
        phone_number = phone_number,
        address = address,
        role = Role.DELIVERYWORKER.value
    ) 

def get_all_workers():
    return User.objects.filter(role = Role.DELIVERYWORKER.value)

def toggle_active_worker(worker_id,is_active):
    worker = User.objects.get(id = worker_id)
    worker.is_active = is_active
    worker.save()        
    return worker

def create_worker(email,first_name,last_name,phone_number):
    return User.objects.create(
        email = email,
        first_name = first_name,
        last_name = last_name,
        phone_number = phone_number,
        role = Role.DELIVERYWORKER.value
    )

def get_worker_obj_by_id(worker_id):
    return User.objects.filter(id = worker_id, role = Role.DELIVERYWORKER.value).first()

def update_worker(worker_id,email,first_name,last_name,phone_number):
    worker = get_worker_obj_by_id(worker_id)
    worker.email = email
    worker.first_name = first_name
    worker.last_name = last_name
    worker.phone_number = phone_number
    worker.save()
    return worker

def get_worker_by_user_obj(user):
    return DeliveryPerson.objects.filter(user = user, is_active = True).first()