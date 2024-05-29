from django.contrib import admin
from .models import Product, Category, Tag, Supplier, StockMovement
from users_account.models import Customer, Review
from cart.models import Order, OrderItem, ShippingStatus, Shipment

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created_at', 'updated_at', 'expire_date', 'is_featured', 'featured_price']
    list_filter = ['available', 'created_at', 'updated_at', 'category', 'is_featured', 'expire_date']
    list_editable = ['price', 'stock', 'available', 'is_featured', 'featured_price']
    search_fields = ['name', 'category__name', 'description', 'tags__name']

    # If you have a slug field in your model, uncomment the line below
    # prepopulated_fields = {'slug': ('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_username', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer__user__username', 'product__name')

    def customer_username(self, obj):
        return obj.customer.user.username
    customer_username.admin_order_field = 'customer'  # Allows column to be sortable by user
    customer_username.short_description = 'Customer'  # Renames column head

# List of models to register
models_to_register = [
    Category,
    Tag,
    Supplier,
    StockMovement,
    Customer,
    Order,
    OrderItem,
    ShippingStatus,
    Shipment,
]

# Register each model if not already registered
for model in models_to_register:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
