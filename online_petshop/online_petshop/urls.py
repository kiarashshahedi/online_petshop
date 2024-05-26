from django.contrib import admin
from django.urls import path, include
#adding media url 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('cart', include('cart.urls')),
    path('users', include('products.urls')),

]

# add media and static directories
urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)