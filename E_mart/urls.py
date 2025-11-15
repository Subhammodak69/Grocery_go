from E_mart.views import *
from django.urls import path

urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('signup/',SignupView.as_view(), name='signup'),
    path('send-otp/',OtpSendView.as_view(), name='send_otp'),
    path('verify-otp/',VerifyOtpView.as_view(), name='verify_otp'),
    
    path('admin/',AdminHomeView.as_view(), name='admin'),
    path('admin/login/',AdminLoginView.as_view(), name="admin_login"),
    path('admin/users/',AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/user/create/',AdminUserCreateView.as_view(), name='admin_user_create'),
    path('admin/user/update/<int:user_id>/',AdminUserUpdateView.as_view(), name='admin_user_update'),
    path('admin/users/toggle-active/',AdminUserToggleActiveView.as_view(), name='admin_user_toggle_active'),
    
    path('admin/posters/',AdminPosterListView.as_view(), name='admin_poster_list'),
    path('admin/poster/create/',AdminPosterCreateView.as_view(), name='admin_poster_create'),
    path('admin/poster/update/<int:poster_id>/',AdminPosterUpdateView.as_view(), name='admin_user_update'),
    path('admin/posters/toggle-active/',AdminPosterToggleActiveView.as_view(), name='admin_user_toggle_active'),

    path('admin/categories/',AdminCategoryListView.as_view(), name='admin_category_list'),
    path('admin/category/create/',AdminCategoryCreateView.as_view(), name='admin_category_create'),
    path('admin/category/update/<int:category_id>/',AdminCategoryUpdateView.as_view(), name='admin_category_update'),
    path('admin/categories/toggle-active/',AdminCategoryToggleActiveView.as_view(), name='admin_category_toggle_active'),

    path('admin/products/',AdminProductListView.as_view(), name='admin_product_list'),
    path('admin/product/create/',AdminProductCreateView.as_view(), name='admin_product_create'),
    path('admin/product/update/<int:product_id>/',AdminProductUpdateView.as_view(), name='admin_product_update'),
    path('admin/products/toggle-active/',AdminProductToggleActiveView.as_view(), name='admin_product_toggle_active'),

    #enduser

    path('api/categories/',ApiGetAllCategory, name='api_get_categories'),
    path('products/<int:category_id>/',CategoryProductList.as_view(), name='category_products'),  
    path('api/products/search/', ProductSearchView.as_view(), name='product-search'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('product/<int:product_id>/',ProductDetailsView.as_view(), name='product_details'), 
    path('product-order/summary/',ProductOrderSummary.as_view(), name='product_order_summary'),
    path('cart-product-order/summary/',ProductsOrderSummaryByCart.as_view(), name='cart_product_order_summary'),
    path('user/cart/',UserCartDetailsView.as_view(), name='user_cart'),
    path('order/create/',OrderCreateView.as_view(),name='order_create'),
    path('order/delete/',OrderDeleteView.as_view(),name='order_delete'),
    path('delete/order/<int:order_id>/',OrderPermanentDeleteView.as_view(),name='order_permanent_delete'), 
    path('orders/',OrderListView.as_view(),name='order_list'),
    path('order/<int:order_id>/',OrderDetailsView.as_view(),name='order_details'),
    path('user/cart/create-data/',UserCartCreateDataView.as_view(), name='user_cart_create_data'),
    path('api/cart/remove-item/<int:cart_id>/',ApiRemoveCartItem.as_view(), name='cart_remove_item'),
    path('api/product-quantity/update/<int:item_id>/', CartItemUpdateView.as_view(), name="cartitem-update"),
    path('wishlist/', WishlistListView.as_view(), name="user_wishlist"),
    path('review/create/', ReviewCreateView.as_view(), name='review_create'),
    path('wishlist/delete-item/<int:wishlist_id>/', WishlistItemDeleteView.as_view(), name="wishlist_item_delete"),
    path('create/payment/<int:order_id>/',PaymentCreateView.as_view(), name='payment_create'),
    path('wishlist/toggle/<int:product_id>/',ToggleWishlistCreateDelete.as_view(), name='wishlist_toggler'),
    path('wishlist/check/<int:product_id>/', CheckWishlistStatus.as_view(), name='check_wishlist'),
    #delivery worker
    path('delivery-worker/',DeliveryWorkerHomeView.as_view(), name='delivery_worker_home'),
    path('admin/delivery-worker/create/',AdminWorkerCreateView.as_view(), name='delivery_worker_create'),
]
