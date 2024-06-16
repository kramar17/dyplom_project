from django.views.generic import TemplateView
from django.db.models import Q
from shop.models import Product, ProductCategory, Manufacturer


class OurShopView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

        return context
