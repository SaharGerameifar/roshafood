import itertools
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.views.generic import (
    ListView,
    CreateView,
)
from .models import Product, OrderItem, Order, Category
from settingSite.models import SiteSettings
from django.views.generic.base import ContextMixin
from django.views.decorators.http import require_POST
from .forms import (
    CartAddProductForm,
    CartUpdateProductForm,
    OrderCheckoutForm,
) 
from django.utils.encoding import uri_to_iri
from .cart import Cart
from django.http import HttpResponse, HttpResponseRedirect
from eshop.settings import MERCHANT
from logger import statistic
from django.contrib import messages
from zeep import Client
from decouple import config

def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


class FormContextMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        ctx = super(FormContextMixin, self).get_context_data(**kwargs)
        ctx['cart_product_from'] = CartAddProductForm()
        return ctx


def navbar(request, *args, **kwargs):
    categories = Category.objects.all()
    site_setting = SiteSettings.objects.first()
    context = {
        'categories': categories,
        'site_setting': site_setting,
    }

    return render(request, 'navbar.html', context)


def footer(request, *args, **kwargs):
    site_setting = SiteSettings.objects.first()
    context = {
        'site_setting': site_setting,
    }

    return render(request, 'footer.html', context)


def home(request):
    context = {}
    return render(request, 'home.html', context)


class ProductList(FormContextMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 6
    queryset = Product.objects.filter(status=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context


class CategoryProductList(FormContextMixin, ListView):
    model = Product
    template_name = 'category_product_list.html'
    paginate_by = 6
    
    def get_queryset(self):
        print(self.kwargs.get('slug'))
        queryset = Product.objects.filter(category__slug=uri_to_iri(self.kwargs.get('slug')))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        try:
            context["product"] = Category.objects.get(slug=uri_to_iri(self.kwargs.get('slug')))
            context['cart_product_form'] = CartAddProductForm()
        except Category.DoesNotExist:
            pass
        return context


def product_detail(request, id):
    product = get_object_or_404(Product , id=id, status=True)
    recommended_products =  product.recommended_product.filter(status=True).distinct()
    context = {
        'product': product,
        'recommended_products':my_grouper(3, recommended_products),
        'cart_product_form': CartAddProductForm(),
    }
    return render(request, 'product_detail.html', context)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 count=cd['count'],
                 update_count=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartUpdateProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 count=cd['count'],
                 update_count=cd['update'])
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_count_from'] = CartUpdateProductForm(initial={'count': item['count'],
                                                                   'update': True})
    return render(request, 'cart.html', {'cart': cart})


def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCheckoutForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         count=item['count'])
            # Clear the cart
            cart.clear()
            return redirect('to_bank', order_id=order.random_order_id)

    else:
        form = OrderCheckoutForm()
    return render(request, 'checkout.html', {'cart': cart,
                                             'form': form})


zarinpall_gateway = config('zarinpall_gateway')
CallbackURL = config('CallbackURL')


def to_bank(request, order_id):
    order = get_object_or_404(Order, random_order_id=order_id)
    description = "روشا فود" 
    email = order.email
    mobile = order.mobile
    order_items = OrderItem.objects.filter(order=order)
    amount = 0
    for item in order_items:
        amount += item.price
    if amount == 0:
        return render(request, 'to_bank.html', {'order_items': order_items})
    order.amount = amount
    order.save()
    client = Client(zarinpall_gateway)
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100 and len(result.Authority) == 36:
        order.authority = str(result.Authority)
        order.save()
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


def callback(request):
    statistic.log(request)
    if request.GET.get('Status') == 'OK':
        authority = str(request.GET['Authority'])
        order = get_object_or_404(Order, authority=authority)
        client = Client(zarinpall_gateway)
        result = client.service.PaymentVerification(MERCHANT, authority, order.amount)
        if result.Status == 100:
            order_items = OrderItem.objects.filter(order=order)
            order.order_status = 1  # Complete
            order.refId = result.RefID
            order.save()
            return render(request, 'callback.html', {'order_items': order_items,
                                                     'refId': order.refId})
        elif result.Status == 101:
            order_items = OrderItem.objects.filter(order=order)
            return render(request, 'callback.html', {'order_items': order_items,
                                                     'refId': order.refId})
        else:
            return HttpResponse('تراکنش ناموفق.\nStatus: ' + str(result.Status) +
                                '<a href="http://roshafood.ir">بازگشت</a>')
    else:
        return HttpResponse('پرداخت توسط کاربر لغو شد' + '<a href="http://roshafood.ir">بازگشت</a>')
