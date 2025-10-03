from E_mart.models import ProductDetails, Product


def get_all_product_details():
    return ProductDetails.objects.all().order_by('id')


def get_product_details_by_id(product_details_id):
    return ProductDetails.objects.filter(id=product_details_id).first()


def product_details_create(product_id, price, stock, size, is_active=True):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        raise ValueError("Invalid product ID")

    return ProductDetails.objects.create(
        product=product,
        price=price,
        stock=stock,
        size=size,
        is_active=is_active
    )


def product_details_update(product_details_id, product_id, price, stock, size, is_active=True):
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
    product_detail.save()
    return product_detail


def toggle_active_product(product_details_id,is_active):
    product_details = ProductDetails.objects.filter(id = product_details_id).first()
    product_details.is_active = is_active
    product_details.save()        
    return product_details

def get_product_details_options_by_id(product_id):
    options = []
    product_details = ProductDetails.objects.filter(product = product_id, is_active = True)
    for item in product_details:
        options.append({
                'id':item.id,
                'size':item.size,
                'price':item.price,
                'stock':item.stock
            })
    return options