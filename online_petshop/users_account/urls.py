from django.urls import path
from .views import RegisterUserView, register_view, verify, LoginView, LogoutView, ReviewCreateView

urlpatterns = [
    
    
    
    path('register/', register_view, name='register_view'),  # OTP registration 
    path('register_user/', RegisterUserView.as_view(), name='register_user_view'),  #  username/password registration 
    path('verify/', verify, name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('review/<int:product_id>/', ReviewCreateView.as_view(), name='review_create'),



]
