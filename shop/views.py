from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import get_user_model
from shop.models import Cart, Product, ProductCategory, Manufacturer, Order, Comment
from .forms import PaymentForm, DeliveryForm, CommentForm

User = get_user_model()


class OurShopView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            # Проверяем, есть ли у пользователя корзина
            if not hasattr(user, 'cart'):
                # Создаем новую корзину для пользователя
                Cart.objects.create(user=user, products={})

        # Получение всех категорий и производителей
        categories = ProductCategory.objects.filter(is_visible=True)
        manufacturers = Manufacturer.objects.filter(is_visible=True)

        # Получение фильтров из GET-запроса
        selected_categories = self.request.GET.getlist('categories')
        selected_manufacturers = self.request.GET.getlist('manufacturers')
        search_query = self.request.GET.get('search', '')

        # Фильтрация продуктов
        products = Product.objects.filter(is_visible=True)

        if selected_categories:
            products = products.filter(category__id__in=selected_categories)

        if selected_manufacturers:
            products = products.filter(manufacturer__id__in=selected_manufacturers)

        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        # Добавление данных в контекст
        context['categories'] = categories
        context['manufacturers'] = manufacturers
        context['products'] = products
        context['selected_categories'] = list(map(int, selected_categories))
        context['selected_manufacturers'] = list(map(int, selected_manufacturers))
        context['search_query'] = search_query
        context['cart'] = user.cart if user.is_authenticated else None

        return context


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        user = request.user

        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            cart.add_product(product, quantity=quantity)

        return redirect('our_shop')


class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        cart = user.cart

        cart_items = []
        total_price = 0

        for product_id, item in cart.products.items():
            product = get_object_or_404(Product, id=product_id)
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total_price': item['quantity'] * float(item['price'])
            })
            total_price += item['quantity'] * float(item['price'])

        context['cart_items'] = cart_items
        context['total_price'] = total_price

        return context

    def post(self, request):
        user = request.user
        cart = user.cart
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        if 'remove_item' in request.POST:
            cart.remove_product(product_id)
        elif 'update_quantity' in request.POST:
            cart.update_product_quantity(product_id, quantity)

        return redirect('cart')


class PaymentView(TemplateView):
    template_name = 'pay.html'
    payment_form_class = PaymentForm
    delivery_form_class = DeliveryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = user.cart

        total_price = sum(item['quantity'] * float(item['price']) for item in cart.products.values())

        context['payment_form'] = self.payment_form_class()
        context['delivery_form'] = self.delivery_form_class()
        context['total_price'] = total_price

        return context

    def post(self, request, *args, **kwargs):
        payment_form = self.payment_form_class(request.POST)
        delivery_form = self.delivery_form_class(request.POST)

        if payment_form.is_valid() and delivery_form.is_valid():
            user = request.user
            cart = user.cart
            total_price = sum(item['quantity'] * float(item['price']) for item in cart.products.values())

            # Сбор данных из формы доставки
            city = delivery_form.cleaned_data['city']
            address = delivery_form.cleaned_data['address']
            comment = delivery_form.cleaned_data['comment']

            products = ''
            for product_id, item in cart.products.items():  # используем .items() для итерации по словарю
                product = get_object_or_404(Product, id=product_id)
                products += f'{product.name} {product.manufacturer}, {item["quantity"]} штук,   '

            # Создаем новый заказ
            order = Order.objects.create(
                user=user,
                products=products,
                total_price=total_price,
                phone_number=user.username,  # Номер телефона берем из self.username
                first_name=user.first_name,
                last_name=user.last_name,
                city=city,
                address=address,
                comment=comment
            )

            # Очистка корзины
            cart.clear_cart()

            # Перенаправление на страницу успешной оплаты
            return redirect('payment_success')

        context = self.get_context_data(payment_form=payment_form, delivery_form=delivery_form)
        return self.render_to_response(context)


class PaymentSuccessView(TemplateView):
    template_name = 'payment_success.html'


class PaymentIsSuccessView(View):
    def get(self, request, *args, **kwargs):
        # Логика здесь, если требуется, например, сохранение данных о успешной оплате
        # в базе данных или отправка уведомления на почту.

        return render(request, 'payment_success.html')


class UpdateCartView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        cart = user.cart
        product_id = request.POST.get('product_id')

        if 'remove_item' in request.POST:
            cart.remove_product(product_id)
        elif 'decrease_quantity' in request.POST:
            cart.update_product_quantity(product_id, -1)
        elif 'increase_quantity' in request.POST:
            cart.update_product_quantity(product_id, 1)

        return redirect('cart')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        context['average_rating'] = self.object.comments.aggregate(Avg('rating'))['rating__avg']
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = self.object
            comment.user = request.user
            comment.save()
            return redirect('product_detail', pk=self.object.pk)

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


@login_required
def add_comment(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        if text and rating:
            Comment.objects.create(product=product, user=request.user, text=text, rating=rating)
    return redirect(reverse('product_detail', args=[pk]))