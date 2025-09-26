from E_mart.models import Wishlist
from E_mart.services import product_service

def toggle_wishlist_create_delete(product_id, user):
    product = product_service.get_product_by_id(product_id)
    wishlist_item = Wishlist.objects.filter(product=product, created_by=user).first()
    if wishlist_item and wishlist_item.is_active:
        wishlist_item.is_active = False
        wishlist_item.save()
        in_wishlist = False
    else:
        if wishlist_item:
            wishlist_item.is_active = True
            wishlist_item.save()
        else:
            Wishlist.objects.create(product=product, created_by=user, is_active=True)
        in_wishlist = True
    return in_wishlist


def is_in_wishlist(product_id, user):
    product = product_service.get_product_by_id(product_id)
    if not user.is_authenticated:
        return False
    return Wishlist.objects.filter(product=product, created_by=user, is_active=True).exists()
