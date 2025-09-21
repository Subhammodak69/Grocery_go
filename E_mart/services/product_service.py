from E_mart.models import Product
from E_mart.services import category_service
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string


def get_all_products():
    return Product.objects.all().order_by('id')

def get_all_active_products():
    return Product.objects.filter(is_active = True)

def get_product_by_id(product_id):
    return Product.objects.filter(id=product_id).first()

def product_create(category_id ,name,description,image_file,price,stock,size):
    category = category_service.get_category_by_id(category_id)
    return Product.objects.create(
        category = category,
        name = name,
        description = description,
        image = get_relative_url_of_product(image_file),
        price = price,
        stock = stock,
        size = size
    )


def product_update(product_id,category_id ,name,description,image_file,price,stock,size):
    category = category_service.get_category_by_id(category_id)
    product = get_product_by_id(product_id)
    if image_file == None:
        product.category = category
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.size = size
    else:
        product.category = category
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.size = size
        product.image = get_relative_url_of_product(image_file)
    return product


def get_relative_url_of_product(photo_file):
    # Save inside app's static/categories folder
    products_dir = os.path.join(settings.BASE_DIR, 'E_mart', 'static', 'images', 'products')
    os.makedirs(products_dir, exist_ok=True)

    file_ext = os.path.splitext(photo_file.name)[1]  # e.g., '.jpg'
    unique_filename = get_random_string(12) + file_ext

    fs = FileSystemStorage(location=products_dir)
    filename = fs.save(unique_filename, photo_file)

    # Relative URL should match STATIC_URL + folder inside app static
    relative_url = f'images/products/{filename}'
    return relative_url


def toggle_active_product(product_id,is_active):
    product = Product.objects.filter(id = product_id).first()
    product.is_active = is_active
    product.save()        
    return product


def get_products_by_category(category_id):
    return Product.objects.filter(category__id =category_id, is_active = True)