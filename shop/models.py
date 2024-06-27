from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __iter__(self):
        for manufacturer in self.manufacturers.filter(is_visible=True):
            yield manufacturer

    class Meta:
        verbose_name = 'Виробник'
        verbose_name_plural = 'Виробники'
        ordering = ['name']


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_visible = models.BooleanField(default=True)
    sort = models.PositiveSmallIntegerField()

    def __iter__(self):
        for product in self.products.filter(is_visible=True):
            yield product

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія товарів'
        verbose_name_plural = 'Категорії товарів'
        ordering = ['-sort']


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_visible = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='manufacturers')
    sort = models.PositiveSmallIntegerField()
    photo = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['sort']

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.JSONField(default=dict, verbose_name='Products in cart')

    def add_product(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.products:
            self.products[product_id]['quantity'] += quantity
        else:
            self.products[product_id] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
            }
        self.save()

    def remove_product(self, product_id):
        product_id = str(product_id)  # Преобразование в строку для ключа словаря
        if product_id in self.products:
            del self.products[product_id]
            self.save()

    def clear_cart(self):
        self.products = {}
        self.save()

    def update_product_quantity(self, product_id, quantity_change):
        product_id = str(product_id)
        if product_id in self.products:
            new_quantity = self.products[product_id]['quantity'] + quantity_change
            if new_quantity > 0:
                self.products[product_id]['quantity'] = new_quantity
            else:
                del self.products[product_id]
            self.save()

    def get_cart_items(self):
        return self.products


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.JSONField()  # Сохранение продуктов и их количества
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)  # Используем CharField для хранения номера телефона
    first_name = models.CharField(max_length=100)  # Имя пользователя
    last_name = models.CharField(max_length=100)   # Фамилия пользователя
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.product}'
