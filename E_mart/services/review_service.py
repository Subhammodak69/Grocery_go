from E_mart.models import Review
from E_mart.services import product_service


def get_all_reviews_by_product_id(product_id):
    product = product_service.get_product_by_id(product_id)
    return Review.objects.filter(product = product, is_active = True)

def get_product_review_data(product_id):
    reviews = get_all_reviews_by_product_id(product_id)
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
