from E_mart.models import DeliveryPerson

def get_all_deliverypersons():
    return DeliveryPerson.objects.all()

def get_deliveryperson(delivery_person_id):
    return DeliveryPerson.objects.get(id = delivery_person_id, is_active = True)

def create_deliveryperson(user):
    return DeliveryPerson.objects.create(
        user=user,
    )
    
def get_available_delivery_boys():
    return DeliveryPerson.objects.filter(is_available = True, is_active = True)

def get_delivery_person_by_id(assigned_to):
    return DeliveryPerson.objects.filter(id= assigned_to, is_available = True, is_active = True).first()