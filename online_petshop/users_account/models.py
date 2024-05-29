from django.db import models
from django.contrib.auth.models import User
from cart import apps
from django.core.validators import RegexValidator

# User
class Customer(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        unique=True
    )   
    
    address = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=128) 
    otp = models.IntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=100)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.user.username

    @property
    def orders(self):
        Order = apps.get_model('cart', 'Order')
        return Order.objects.filter(customer=self)


# Review
class Review(models.Model):
    product = models.ForeignKey('products.Product', related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.product.name} - {self.rating}"


# Rating
class Rating(models.Model):
    product = models.ForeignKey('products.Product', related_name='ratings', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='ratings', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return f"{self.product.name} - {self.score}"
