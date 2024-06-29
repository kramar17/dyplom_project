from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Manufacturer(models.Model):
    """
    Manufacturer model represents a product manufacturer.

    Attributes:
        name (str): The name of the manufacturer.
        is_visible (bool): Whether the manufacturer is visible.
    """

    name = models.CharField(max_length=255, unique=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Виробник'
        verbose_name_plural = 'Виробники'
        ordering = ['name']


class ProductCategory(models.Model):
    """
    ProductCategory model represents a category of products.

    Attributes:
        name (str): The name of the category.
        slug (str): The slug for the category.
        is_visible (bool): Whether the category is visible.
        sort (int): The sorting order of the category.
    """

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_visible = models.BooleanField(default=True)
    sort = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категорія товарів'
        verbose_name_plural = 'Категорії товарів'
        ordering = ['-sort']


class Product(models.Model):
    """
    Product model represents a product.

    Attributes:
        id (int): The unique identifier for the product.
        name (str): The name of the product.
        description (str): The description of the product.
        price (Decimal): The price of the product.
        is_visible (bool): Whether the product is visible.
        is_available (bool): Whether the product is available.
        category (ProductCategory): The category to which the product belongs.
        manufacturer (Manufacturer): The manufacturer of the product.
        sort (int): The sorting order of the product.
        photo (ImageField): The photo of the product.
    """

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

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['sort']


class Cart(models.Model):
    """
    Cart model represents a user's shopping cart.

    Attributes:
        user (User): The user associated with the cart.
        products (dict): JSON field storing products in the cart.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.JSONField(default=dict, verbose_name='Products in cart')

    def add_product(self, product: Product, quantity: int = 1):
        """
        Add a product to the cart.

        Args:
            product (Product): The product to add.
            quantity (int): The quantity of the product to add.
        """
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

    def remove_product(self, product_id: int):
        """
        Remove a product from the cart.

        Args:
            product_id (int): The ID of the product to remove.
        """
        product_id = str(product_id)
        if product_id in self.products:
            del self.products[product_id]
            self.save()

    def clear_cart(self):
        """Clear all products from the cart."""
        self.products = {}
        self.save()

    def update_product_quantity(self, product_id: int, quantity_change: int):
        """
        Update the quantity of a product in the cart.

        Args:
            product_id (int): The ID of the product to update.
            quantity_change (int): The change in quantity (+/-).
        """
        product_id = str(product_id)
        if product_id in self.products:
            new_quantity = self.products[product_id]['quantity'] + quantity_change
            if new_quantity > 0:
                self.products[product_id]['quantity'] = new_quantity
            else:
                del self.products[product_id]
            self.save()

    def get_cart_items(self) -> dict:
        """
        Retrieve all products in the cart.

        Returns:
            dict: Dictionary of products in the cart.
        """
        return self.products


class Order(models.Model):
    """
    Order model represents a user's order.

    Attributes:
        id (int): The unique identifier for the order.
        user (User): The user who placed the order.
        products (dict): JSON field storing products and their quantities.
        total_price (Decimal): The total price of the order.
        phone_number (str): The phone number associated with the order.
        first_name (str): The first name of the user placing the order.
        last_name (str): The last name of the user placing the order.
        city (str): The city for delivery.
        address (str): The delivery address.
        comment (str): Any additional comments for the order.
        created_at (DateTime): The date and time when the order was created.
        is_processed (bool): Whether the order has been processed.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)


class Comment(models.Model):
    """
    Comment model represents a comment on a product.

    Attributes:
        product (Product): The product being commented on.
        user (User): The user who wrote the comment.
        text (str): The text content of the comment.
        rating (int): The rating given by the user.
        created_at (DateTime): The date and time when the comment was created.
    """

    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Comment by {self.user} on {self.product}'
