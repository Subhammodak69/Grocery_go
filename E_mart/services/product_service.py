from E_mart.models import Product
from E_mart.services import category_service
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
import random



def get_all_products():
    return Product.objects.all().order_by('id')

def get_random_product_by_id(product_id):
    products = list(Product.objects.filter(product=product_id, is_active=True).values('price','size'))
    if products:
        return random.choice(products)
    return None

def get_all_active_products():
    products = Product.objects.filter(is_active = True)
    products_data = [
        {
            'id':p.id,
            'name':p.name,
            'image':p.image,
            'product_options':product_details_service.get_product_details_options_by_id(p.id),
        }
        for p in products
    ] 
    return products_data

def get_product_by_id(product_id):
    return Product.objects.filter(id=product_id).first()

def product_create(category_id ,name,description,image_file):
    category = category_service.get_category_by_id(category_id)
    return Product.objects.create(
        category = category,
        name = name,
        description = description,
        image = get_relative_url_of_product(image_file)
    )


def product_update(product_id,category_id ,name,description,image_file):
    category = category_service.get_category_by_id(category_id)
    product = get_product_by_id(product_id)
    if image_file == None:
        product.category = category
        product.name = name
        product.description = description
    else:
        product.category = category
        product.name = name
        product.description = description
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
    products = Product.objects.filter(category = category_id, is_active = True)
    products_data = [
        {
            'id':p.id,
            'name':p.name,
            'image':p.image,
            'product_options':product_details_service.get_product_details_options_by_id(p.id),
        }
        for p in products
    ] 
    return products_data

def product_all_data_by_details_id(product_details_id):
    item = Product.objects.filter(id = product_details_id, is_active = True).first()
    data = {
        'id':item.id,
        'name':item.product.name,
        'size':item.size,
        'price':item.price,
        'stock':item.stock,
        'image':item.product.image,
        'description':item.product.description
    }
    return data
    