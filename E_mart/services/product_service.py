from E_mart.models import Product,ProductDetails
from E_mart.services import category_service
import random


def get_all_products():
    return Product.objects.all().order_by('id')

def get_random_product_by_id(product_id):
    products = list(ProductDetails.objects.filter(product=product_id, is_active=True).values('price','size'))
    if products:
        return random.choice(products)
    return None

def get_all_active_products():
    products = Product.objects.filter(is_active = True)
    products_data = [
        {
            'id':p.id,
            'name':p.name,
            'product_details':get_random_product_by_id(p.id),
        }
        for p in products
    ] 
    print(products_data)
    return products_data

def get_product_by_id(product_id):
    return Product.objects.filter(id=product_id).first()

def product_create(category_id ,name,description):
    category = category_service.get_category_by_id(category_id)
    return Product.objects.create(
        category = category,
        name = name,
        description = description,
    )


def product_update(product_id,category_id ,name,description):
    category = category_service.get_category_by_id(category_id)
    product = get_product_by_id(product_id)
    product.category = category
    product.name = name
    product.description = description
    return product


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
            'product_details':get_random_product_by_id(p.id),
        }
        for p in products
    ] 
    return products_data

def get_product_data_by_id(product_id):
    return  Product.objects.filter(id=product_id, is_active = True).first()
    