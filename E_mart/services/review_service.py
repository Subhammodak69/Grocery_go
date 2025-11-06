from E_mart.models import Review
from E_mart.services import product_service
import os
from django.conf import settings
import base64
import re
from django.utils.crypto import get_random_string


def get_all_reviews_by_product_id(product_id):
    product = product_service.get_product_by_id(product_id)
    return Review.objects.filter(product = product, is_active = True)

def get_product_review_data(product_id):
    reviews = get_all_reviews_by_product_id(product_id).order_by('-created_at')
    review_data = [
        {
            'id':review.id,
            'product_id':review.product.id,
            'created_by':f"{review.user.first_name} {review.user.last_name}",
            'review_image':review.review_image,
            'review_text':review.review_text,
            'colored_stars':range(review.review_stars),
            'uncolored_stars':range(5-review.review_stars),
            'created_at':review.created_at
        }
        for review in reviews
    ]
    return review_data

def get_rating_by_product_id(product_id):
    reviews = get_all_reviews_by_product_id(product_id)
    total_review_star = sum(review.review_stars for review in reviews)
    if not len(reviews) == 0:
        rated_stars =round(total_review_star/len(reviews))
    else:
        rated_stars = 0
    rating_data = {
        'rated_stars':range(rated_stars),
        'ratings':len(reviews),
        'unrated_stars':range(5-rated_stars)
    }
    return rating_data


def create_review(product_id, user, text, photo, stars):
    stars = int(stars)  # convert stars to integer

    product = product_service.get_product_by_id(product_id)
    if photo:
        review = Review.objects.create(
            product=product,
            user=user,
            review_text=text,
            review_image=get_relative_url_of_review_image(photo),
            review_stars=stars
        )
    else:
        review = Review.objects.create(
            product=product,
            user=user,
            review_text=text,
            review_stars=stars
        )

    return {
    'id': review.id,
    'review': review.review_text,
    'photo': review.review_image if review.review_image else '',
    'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    'created_by_fullname': f"{review.user.first_name} {review.user.last_name}" if review.user else 'Anonymous',
    'stars_range': list(range(review.review_stars)),         # convert to list
    'empty_stars_range': list(range(5 - review.review_stars)) # convert to list
}



def get_relative_url_of_review_image(base64_data):
    # base64_data expected in form 'data:image/png;base64,iVBORw0K...'

    # Extract file extension and base64 string with regex
    format_match = re.match(r'data:image/(?P<ext>.+?);base64,(?P<data>.+)', base64_data)
    if not format_match:
        raise ValueError("Invalid image data")

    ext = format_match.group('ext')  # e.g., 'png', 'jpeg'
    data = format_match.group('data')

    # Decode base64 data to binary
    decoded_file = base64.b64decode(data)

    # Generate unique filename
    unique_filename = get_random_string(12) + '.' + ext

    # Define directory to save
    categories_dir = os.path.join(settings.BASE_DIR, 'E_mart', 'static', 'images', 'reviews')
    os.makedirs(categories_dir, exist_ok=True)

    filepath = os.path.join(categories_dir, unique_filename)

    # Save binary content to file
    with open(filepath, 'wb') as f:
        f.write(decoded_file)

    # Return relative URL for static serving
    return f'images/reviews/{unique_filename}'
