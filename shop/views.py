from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from shop.models import Category, Product


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
        print(self.object)
        products = Product.objects.filter(category=self.object)
        context['products'] = products
        return context


def add_to_cart(request, product_id, category_id):
    # request.session['cart'] = []
    cart = request.session['cart']
    items = [i['product'] for i in cart]
    if product_id in items:
        for i in cart:
            if i['product'] == product_id:
                i['quantity'] += 1
                break
    else:
        cart_item = {'product': product_id, 'quantity': 1}
    cart.append(1)
    request.session.modifid = True
    product = Product.objects.get(pk=product_id)
    category = product.category.pk
    print(cart)
    return redirect('category_detail', category_id)


def cart(request):
    my_cart = request.session.get('cart')
    my_cart_context = []
    for item in my_cart:
        my_cart_item = {}
        my_cart_item['product'] = Product.objects.get(pk=item['product'])
        my_cart_context.append(my_cart_item)

    print(my_cart_item)
    context = {'cart': cart}
    return render(request, 'shop/cart.html', context)

