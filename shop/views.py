from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from shop.models import Cart, Product, ProductCategory, Manufacturer

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

