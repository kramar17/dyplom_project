from django.db import models


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
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_visible = models.BooleanField(default=True)
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
