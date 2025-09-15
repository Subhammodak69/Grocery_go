from E_mart.models import DeliveryPerson

def get_all_deliverypersons():
    return DeliveryPerson.objects.all()

def get_deliveryperson(delivery_person_id):
    return DeliveryPerson.objects.get(id = delivery_person_id, is_active = True)

def create_deliveryperson(user):
    return DeliveryPerson.objects.create(
        user=user,
    )
    