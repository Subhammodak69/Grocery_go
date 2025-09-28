from E_mart.models import ProductDetails, Product
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string


def get_all_product_details():
    return ProductDetails.objects.all().order_by('id')


def get_product_details_by_id(product_details_id):
    return ProductDetails.objects.filter(id=product_details_id).first()


def product_details_create(product_id, price, stock, size, image_file, is_active=True):
    print("aslam")
    product = Product.objects.filter(id=product_id).first()
    if not product:
        raise ValueError("Invalid product ID")
    print("helloo")
    image_url = get_relative_url_of_product_details(image_file)
    print(image_url)
    return ProductDetails.objects.create(
        product=product,
        price=price,
        stock=stock,
        size=size,
        image=image_url,
        is_active=is_active
    )


def product_details_update(product_details_id, product_id, price, stock, size, image_file=None, is_active=True):
    product_detail = get_product_details_by_id(product_details_id)
    if not product_detail:
        raise ValueError("Invalid product details ID")

    product = Product.objects.filter(id=product_id).first()
    if not product:
        raise ValueError("Invalid product ID")

    product_detail.product = product
    product_detail.price = price
    product_detail.stock = stock
    product_detail.size = size
    product_detail.is_active = is_active

    if image_file:
        product_detail.image = get_relative_url_of_product_details(image_file)

    product_detail.save()
    return product_detail


def get_relative_url_of_product_details(photo_file):
    # Save inside app's static/images/product_details folder
    product_details_dir = os.path.join(settings.BASE_DIR, 'E_mart', 'static', 'images', 'product_details')
    os.makedirs(product_details_dir, exist_ok=True)

    file_ext = os.path.splitext(photo_file.name)[1]  # e.g., '.jpg'
    unique_filename = get_random_string(12) + file_ext

    fs = FileSystemStorage(location=product_details_dir)
    filename = fs.save(unique_filename, photo_file)

    # Return relative URL used in templates: STATIC_URL + folder path
    relative_url = f'images/product_details/{filename}'
    return relative_url


def toggle_active_product(product_details_id,is_active):
    product_details = ProductDetails.objects.filter(id = product_details_id).first()
    product_details.is_active = is_active
    product_details.save()        
    return product_details
