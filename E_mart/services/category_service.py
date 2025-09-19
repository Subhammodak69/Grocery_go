from E_mart.models import Category
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string

def get_all_categories():
    return Category.objects.all().order_by('id')

def get_category_by_id(category_id):
    return Category.objects.filter(id= category_id).first()

def category_create(name, description, photo_file):
    relative_url = get_relative_url_of_category(photo_file)
    return Category.objects.create(
        name=name,
        description=description,
        image=relative_url,
    )

def toggle_active_category(category_id,is_active):
    category = Category.objects.filter(id = category_id).first()
    category.is_active = is_active
    category.save()        
    return category
    
def category_update(category_id,name, description, image_file):
    category = Category.objects.get(id=category_id)
    if image_file == None:
        category.name = name
        category.description = description
        category.save()
        return category
    category.name = name
    category.description = description
    category.image = get_relative_url_of_category(image_file)
    category.save()
    return category

def get_relative_url_of_category(photo_file):
    # Save inside app's static/categories folder
    categories_dir = os.path.join(settings.BASE_DIR, 'E_mart', 'static', 'categories')
    os.makedirs(categories_dir, exist_ok=True)

    file_ext = os.path.splitext(photo_file.name)[1]  # e.g., '.jpg'
    unique_filename = get_random_string(12) + file_ext

    fs = FileSystemStorage(location=categories_dir)
    filename = fs.save(unique_filename, photo_file)

    # Relative URL should match STATIC_URL + folder inside app static
    relative_url = f'categories/{filename}'
    return relative_url