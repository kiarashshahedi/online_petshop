from django.db import models
from django.urls import reverse


#category of products
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank = True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name 
        
        
#product class         
class Product(models.Model):
    
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)  # عکس
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField() # تعداد موجودی
    available = models.BooleanField(default=True) # موجودی
    created_at = models.DateTimeField(auto_now_add=True) # زمان ایجاد
    updated_at = models.DateTimeField(auto_now=True) # زمان بروزرسانی
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # وزن بر اساس کیلوگرم
    dimensions = models.CharField(max_length=100, blank=True)  # ابعاد به صورت متنی
    manufacturer = models.CharField(max_length=255, blank=True)  # اسم سازنده (برند)
    warranty = models.CharField(max_length=255, blank=True)  # اطلاعات گارانتی
    color = models.CharField(max_length=50, blank=True)  # رنگ محصول
    material = models.CharField(max_length=100, blank=True)  # نوع مواد
    breed_size = models.CharField(max_length=50, blank=True)  # اندازه نژاد مناسب (برای محصولات حیوان خانگی)
    life_stage = models.CharField(max_length=50, blank=True)  # مرحله زندگی مناسب (سن)
    flavor = models.CharField(max_length=50, blank=True)  # طعم دهنده (برای غذای حیوانات خانگی)
    nutritional_info = models.TextField(blank=True)  # اطلاعات تغذیه ای
    recommended_usage = models.TextField(blank=True)  # دستورالعمل استفاده توصیه شده
    expire_date = models.DateField(null=True, blank=True)  # تاریخ انقضا
    origin_country = models.CharField(max_length=100, blank=True)  # کشور سازنده
    tags = models.ManyToManyField('Tag', blank=True)  # برچسب ها برای جستجو و فیلتر
    is_featured = models.BooleanField(default=False) #تخفیف
    featured_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        
        
    def __str__(self):
        return self.name

    @property
    def display_price(self):
        return self.featured_price if self.is_featured and self.featured_price else self.price
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])




# tags
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        
        
    def __str__(self):
        return self.name




# برای ردیابی حرکت سهام و تامین کنندگان و مدیریت موجودی تعداد کالای تامین شده
class Supplier(models.Model):
    
    name = models.CharField(max_length=255)
    contact_info = models.TextField(blank=True)
    
    
    
    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        
        
    def __str__(self):
        return self.name
    
    
    
    
    
       
class StockMovement(models.Model):
    
    product = models.ForeignKey(Product, related_name='stock_movements', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=50, choices=(('IN', 'In'), ('OUT', 'Out')))
    date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, related_name='stock_movements', on_delete=models.SET_NULL, null=True, blank=True)
     
     
     
     
    class Meta:
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"
        
        
        
    def __str__(self):
        return f"{self.product.name} - {self.movement_type} - {self.quantity}"
     



