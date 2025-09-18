from E_mart.models import Poster
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string

def get_all_posters():
    return Poster.objects.all()

def get_poster_by_id(poster_id):
    return Poster.objects.filter(id= poster_id).first()

def poster_create(title, description, photo_file, start_date, end_date):
    relative_url = get_relative_url_of_poster(photo_file)
    return Poster.objects.create(
        title=title,
        description=description,
        image=relative_url,
        start_date=start_date,
        end_date=end_date
    )

def toggle_active_poster(poster_id,is_active):
    poster = Poster.objects.filter(id = poster_id).first()
    poster.is_active = is_active
    poster.save()        
    return poster
    
def poster_update(poster_id,title, description, image_file, start_date, end_date):
    poster = Poster.objects.get(id=poster_id)
    poster.title = title
    poster.description = description
    poster.image = get_relative_url_of_poster(image_file)
    poster.start_date = start_date
    poster.end_date = end_date
    poster.save()
    return poster

def get_relative_url_of_poster(photo_file):
    # Save inside app's static/posters folder
    posters_dir = os.path.join(settings.BASE_DIR, 'E_mart', 'static', 'posters')
    os.makedirs(posters_dir, exist_ok=True)

    file_ext = os.path.splitext(photo_file.name)[1]  # e.g., '.jpg'
    unique_filename = get_random_string(12) + file_ext

    fs = FileSystemStorage(location=posters_dir)
    filename = fs.save(unique_filename, photo_file)

    # Relative URL should match STATIC_URL + folder inside app static
    relative_url = f'posters/{filename}'
    return relative_url