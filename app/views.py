from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Item, Category, Order, OrderItem
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('shop')
            else:
                return render(request, 'app/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('shop')

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
        if not cart:
            return redirect('cart')

        order = Order.objects.create()

        for item_id, item in cart.items():
            OrderItem.objects.create(
                ordered=order,
                item_id=item_id,
                quantity=item['quantity'],
                price=item['price']
            )

        request.session['cart'] = {}

        return redirect('order_confirmation', order_id=order.id)
    return redirect('cart')

class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ShopPageView(ListView):
    model = Item
    template_name = 'app/shop.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        category_id = self.request.GET.get('category')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() 
        cart = self.request.session.get('cart', {})
        context['cart_count'] = sum(item['quantity'] for item in cart.values())
        return context
    
class CartPageView(TemplateView):
    template_name = 'app/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})

        for item_id, item in cart.items():
            item['sub_total'] = item['price'] * item['quantity']

        context['cart_items'] = cart
        context['total_price'] = sum(item['price'] * item['quantity'] for item in cart.values())
        context['items'] = Item.objects.all()
        return context

class CheckoutPageView(TemplateView):
    template_name = 'app/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        context['order_items'] = order.items.all()
        
        total_price = 0

        for item in context['order_items']:
            item.sub_total = item.quantity * item.price
            total_price += item.sub_total
        context['total_price'] = total_price
        return context

class OrderConfirmationView(TemplateView):
    template_name = 'app/order_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        context['order_items'] = order.items.all()

        for item in context['order_items']:
            item.sub_total = item.quantity * item.price
        return context
    
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        order = get_object_or_404(Order, id=order_id)

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        address = request.POST.get('address', '').strip()
        contact = request.POST.get('contact', '').strip()

        order.first_name = first_name
        order.last_name = last_name
        order.address = address
        order.contact = contact
        order.save()

        return redirect('checkout', order_id=order.id)

@method_decorator(login_required, name='dispatch')
class AddItemView(CreateView):
    model = Item
    fields = ['title', 'price', 'stock', 'category', 'image']
    template_name = 'app/item.html'
    success_url = reverse_lazy('shop')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ItemEditView(UpdateView):
    model = Item
    fields = ['title', 'price', 'stock', 'category', 'image']
    template_name = 'app/item_edit.html'
    success_url = reverse_lazy('shop')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'app/item_delete.html'
    success_url = reverse_lazy('shop')