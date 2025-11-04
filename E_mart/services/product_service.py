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
    data = [
        {
            'id':product.id,
            'name':product.name,
            'size':product.size,
            'image':product.image,
            'price':product.price,
            'original_price':product.original_price,
            'description':product.description,
            'discount':get_product_offer_by_id(product.id),
            'stock':product.stock
        }
        for product in products
    ]

    return data
   

def get_product_by_id(product_id):
    return Product.objects.filter(id=product_id).first()

def get_product_data_by_id(product_id):
    product = Product.objects.filter(id=product_id).first()
    product_data = {
        'id':product.id,
        'image':product.image,
        'price':product.price,
        'original_price':product.original_price,
        'stock':product.stock,
        'size':product.size,
        'name':product.name,
        'description':product.description,
        'discount':get_product_offer_by_id(product.id)
    }
    return product_data

def product_create(category_id ,name,size,price,original_price,stock,description,image_file):
    category = category_service.get_category_by_id(category_id)
    return Product.objects.create(
        category = category,
        name = name,
        size = size,
        price = price,
        original_price = original_price,
        stock = stock,
        description = description,
        image = get_relative_url_of_product(image_file)
    )


def product_update(product_id,category_id ,name,size,price,original_price,stock,description,image_file):
    category = category_service.get_category_by_id(category_id)
    product = get_product_by_id(product_id)
    if image_file == None:
        product.category = category
        product.name = name
        product.size = size
        product.price = price
        product.original_price = original_price
        product.stock = stock
        product.description = description
        product.save()

    else:
        product.category = category
        product.name = name
        product.size = size
        product.price = price
        product.original_price = original_price
        product.stock = stock
        product.description = description
        product.image = get_relative_url_of_product(image_file)
        product.save()

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
    data = [
        {
            'id':product.id,
            'name':product.name,
            'size':product.size,
            'image':product.image,
            'price':product.price,
            'original_price':product.original_price,
            'description':product.description,
            'discount':get_product_offer_by_id(product.id),
            'stock':product.stock
        }
        for product in products
    ]

    return data
    
def get_product_offer_by_id(product_id):
    product = Product.objects.get(id=product_id,is_active = True)
    discount = ((product.original_price - product.price)/product.original_price)*100
    return discount    

