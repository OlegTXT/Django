from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.core.mail import send_mail

from shop.models import Category, Product, Cart, CartItem


def category_list(request):
    category_list = Category.objects.all()
    context = {"category_list": category_list}
    return render(request, 'shop/category_list.html', context)


class Category_detail(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        products = Product.objects.filter(category=self.object)
        context['products'] = products
        return context


def add_to_cart(request, product_id):
    if not request.session.get('cart'):
        request.session['cart'] = []
    cart = request.session['cart']
    items = [i['product'] for i in cart]
    if product_id in items:
        for i in cart:
            if i['product'] == product_id:
                i['quantity'] += 1
                break
    else:
        cart_item = {
            "product": product_id,
            "quantity": 1
        }
        cart.append(cart_item)

    request.session.modified = True
    product = Product.objects.get(pk=product_id)
    category_id = product.category.pk
    messages.add_message(request, messages.INFO, f"Product {product.title} added to cart!")
    return redirect('category_detail', category_id)


def cart(request):
    my_cart = request.session.get('cart', [])
    if request.method == 'POST':
        cart_item = request.POST.get('cart_item')
        if request.POST.get('add'):
            for i in my_cart:
                if i['product'] == int(cart_item):
                    i['quantity'] += 1
                    break
        elif request.POST.get('remove'):
            for i in my_cart:
                if i['product'] == int(cart_item):
                    i['quantity'] -= 1
                    if i['quantity'] == 0:
                        my_cart.remove(i)
                    break
            messages.add_message(request, messages.WARNING, f"Product decreased successfully")
        request.session.modified = True
        return redirect('cart')  # Решается проблема повторной отправки формы
    my_cart_context = []
    total_price = 0
    for item in my_cart:
        my_cart_item = {}
        my_cart_item['product'] = Product.objects.get(pk=item['product'])
        my_cart_item['quantity'] = item['quantity']
        my_cart_item['total'] = float(my_cart_item['product'].price * my_cart_item['quantity'])
        total_price += my_cart_item['total']
        my_cart_context.append(my_cart_item)
    processed_carts = []
    if request.user.is_authenticated:
        processed_carts = Cart.objects.filter(user=request.user)
    context = {'cart_items': my_cart_context, 'total_price': total_price, 'processed_carts': processed_carts}
    return render(request, 'shop/cart.html', context)


@login_required
def checkout(request):
    if request.method == 'POST':
        cart_model = Cart.objects.create(user=request.user)
        cart = request.session.get('cart', [])
        for i in cart:
            cart_item = CartItem.objects.create(
                product=Product.objects.get(pk=i['product']),
                count=i['quantity']
            )
            cart_model.items.add(cart_item)
        full_name = request.POST['full_name']
        address = request.POST['address']
        request.session['cart'] = []
        request.session.modified = True
        send_mail(
            "Order details",
            f"{full_name} get order to {address}.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )
        return redirect('category_list')
    return render(request, 'shop/checkout.html')
