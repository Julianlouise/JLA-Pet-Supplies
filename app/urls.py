from django.urls import path
from .views import HomePageView, AboutPageView, ShopPageView, CartPageView, OrderConfirmationView, add_to_cart, update_cart, remove_from_cart, get_cart_data

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('shop/', ShopPageView.as_view(), name='shop'),
    path('cart/', CartPageView.as_view(), name='cart'),
    path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', update_cart, name='update_cart'),
    path('remove-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('get-cart-data/', get_cart_data, name='get_cart_data'),
    path('order-confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),
]