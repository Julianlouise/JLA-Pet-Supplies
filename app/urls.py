from django.urls import path
from .views import HomePageView, AboutPageView, ShopPageView, CartPageView, CheckoutPageView, OrderConfirmationView, AddItemView, ItemEditView, ItemDeleteView, add_to_cart, update_cart, remove_from_cart, get_cart_data, signup, login_view, logout_view
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('shop/', ShopPageView.as_view(), name='shop'),
    path('cart/', CartPageView.as_view(), name='cart'),
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('update_cart/<int:item_id>/', update_cart, name='update_cart'),
    path('remove-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('get-cart-data/', get_cart_data, name='get_cart_data'),
    path('checkout/<int:order_id>/', CheckoutPageView.as_view(), name='checkout'),
    path('order_confirmation/<int:order_id>/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('process_order/', views.process_order, name='process_order'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('add-item/', AddItemView.as_view(), name='add_item'),
    path('item/<int:pk>/edit/', ItemEditView.as_view(), name='item_edit'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
]