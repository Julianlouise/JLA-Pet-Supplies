from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Item, Category, Order, OrderItem
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

def add_to_cart(request, item_id):
    if request.method == "POST":

        item = get_object_or_404(Item, id=item_id)
        cart = request.session.get('cart', {})
        
        add_quantity = int(request.POST.get('quantity', 1))

        if str(item_id) in cart:
            if cart[str(item_id)]['quantity'] + add_quantity <= item.stock:
                cart[str(item_id)]['quantity'] += add_quantity
            else:
                return JsonResponse({'error': 'Item out of stock!'}, status=400)
        else:
            if add_quantity <= item.stock:
                cart[str(item_id)] = {
                    'title': item.title,
                    'price': float(item.price),
                    'quantity': add_quantity,
                    'image': item.image.url if item.image else None,
                }
            else:
                return JsonResponse({'error': 'Item out of stock!'}, status=400)

        item.stock -= add_quantity
        item.save()
        request.session['cart'] = cart
        return redirect('shop')

def update_cart(request, item_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        item = get_object_or_404(Item, id=item_id)
        quantity = int(request.POST.get('quantity', 1))

        if str(item_id) in cart:
            old_quantity = cart[str(item_id)]['quantity']
            difference = quantity - old_quantity

            if difference > 0 and difference > item.stock:
                return JsonResponse({'error': 'Not enough stock available'}, status=400)

            item.stock -= difference
            item.save()

            if quantity > 0:
                cart[str(item_id)]['quantity'] = quantity
            else:
                cart.pop(str(item_id), None)
            request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item = get_object_or_404(Item, id=item_id)

    if str(item_id) in cart:
        remove_quantity = cart[str(item_id)]['quantity']
        item.stock += remove_quantity
        item.save()
        cart.pop(str(item_id), None)
        request.session['cart'] = cart
    return redirect('cart')

def get_cart_data(request):
    cart = request.session.get('cart', {})
    return JsonResponse({'cart_items': list(cart.values())})

def process_order(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        name = request.POST['title']
        address = request.POST['address']
        contact = request.POST['contact']
        request.session['cart'] = {}
    return redirect('order_confirmation')

class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ShopPageView(TemplateView):
    template_name = 'app/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')
        if category_id:
            context['items'] = Item.objects.filter(category_id=category_id)
        else:
            context['items'] = Item.objects.all()
        context['categories'] = Category.objects.all()
        cart = self.request.session.get('cart', {})
        context['cart_count'] = sum(item['quantity'] for item in cart.values())
        return context
    
class CartPageView(TemplateView):
    template_name = 'app/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        context['cart_items'] = cart
        context['total_price'] = sum(item['price'] * item['quantity'] for item in cart.values())
        context['items'] = Item.objects.all()
        return context

class OrderConfirmationView(TemplateView):
    template_name = 'app/order_confirmation.html'