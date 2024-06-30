from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import get_user_model

from djangoProject1.loger import shop_logger
from shop.models import Cart, Product, ProductCategory, Manufacturer, Order, Comment
from .forms import PaymentForm, DeliveryForm, CommentForm

User = get_user_model()


class OurShopView(TemplateView):
    """View for displaying the main shop page."""

    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        """Retrieve context data for the shop view."""
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            if not hasattr(user, 'cart'):
                Cart.objects.create(user=user, products={})

        categories = ProductCategory.objects.filter(is_visible=True)
        manufacturers = Manufacturer.objects.filter(is_visible=True)

        selected_categories = self.request.GET.getlist('categories')
        selected_manufacturers = self.request.GET.getlist('manufacturers')
        search_query = self.request.GET.get('search', '')

        products = Product.objects.filter(is_visible=True)

        if selected_categories:
            products = products.filter(category__id__in=selected_categories)

        if selected_manufacturers:
            products = products.filter(manufacturer__id__in=selected_manufacturers)

        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        context['categories'] = categories
        context['manufacturers'] = manufacturers
        context['products'] = products
        context['selected_categories'] = list(map(int, selected_categories))
        context['selected_manufacturers'] = list(map(int, selected_manufacturers))
        context['search_query'] = search_query
        context['cart'] = user.cart if user.is_authenticated else None

        return context


class AddToCartView(View):
    """View for adding products to the cart."""

    def post(self, request, product_id):
        """Handle POST request to add a product to the cart."""
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        user = request.user

        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            cart.add_product(product, quantity=quantity)

        return redirect('our_shop')


class CartView(TemplateView):
    """View for displaying the cart."""

    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        """Retrieve context data for the cart view."""
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
        """Handle POST request to update the cart."""
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
    """View for handling payment process."""

    template_name = 'pay.html'
    payment_form_class = PaymentForm
    delivery_form_class = DeliveryForm

    def get_context_data(self, **kwargs):
        """Retrieve context data for the payment view."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = user.cart

        total_price = sum(item['quantity'] * float(item['price']) for item in cart.products.values())

        context['payment_form'] = self.payment_form_class()
        context['delivery_form'] = self.delivery_form_class()
        context['total_price'] = total_price

        return context

    def post(self, request, *args, **kwargs):
        """Handle POST request for processing payment."""
        payment_form = self.payment_form_class(request.POST)
        delivery_form = self.delivery_form_class(request.POST)

        if payment_form.is_valid() and delivery_form.is_valid():
            user = request.user
            cart = user.cart
            total_price = sum(item['quantity'] * float(item['price']) for item in cart.products.values())

            city = delivery_form.cleaned_data['city']
            address = delivery_form.cleaned_data['address']
            comment = delivery_form.cleaned_data['comment']

            products = ''
            for product_id, item in cart.products.items():
                product = get_object_or_404(Product, id=product_id)
                products += f'{product.name} {product.manufacturer}, {item["quantity"]} штук,   '

            order = Order.objects.create(
                user=user,
                products=products,
                total_price=total_price,
                phone_number=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                city=city,
                address=address,
                comment=comment
            )

            shop_logger.info(f"Замовлення завершено. Загальна сума: {total_price}. "
                             f"Користувач: {user.username}. Адреса доставки: {city}, {address}. "
                             f"Товари: {products}")

            cart.clear_cart()

            return redirect('payment_success')

        context = self.get_context_data(payment_form=payment_form, delivery_form=delivery_form)
        return self.render_to_response(context)


class PaymentSuccessView(TemplateView):
    """View for displaying payment success page."""

    template_name = 'payment_success.html'


class PaymentIsSuccessView(View):
    """Placeholder view for indicating payment success (educational purpose)."""

    def get(self, request, *args, **kwargs):
        """Handle GET request."""
        return render(request, 'payment_success.html')


class UpdateCartView(View):
    """View for updating cart items."""

    def post(self, request, *args, **kwargs):
        """Handle POST request to update cart."""
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
    """View for displaying product details."""

    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """Retrieve context data for product detail view."""
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        context['average_rating'] = self.object.comments.aggregate(Avg('rating'))['rating__avg']
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST request to add a comment."""
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
    """View function for adding a comment to a product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        if text and rating:
            Comment.objects.create(product=product, user=request.user, text=text, rating=rating)
    return redirect(reverse('product_detail', args=[pk]))
