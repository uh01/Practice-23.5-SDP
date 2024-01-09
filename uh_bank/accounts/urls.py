from django.urls import path
from . import views
from .views import UserRegistrationView, UserLoginView, UserLogoutView,UserBankAccountUpdateView, UserPasswordChangeView
 
urlpatterns = [
    path('signin/', UserRegistrationView.as_view(), name='signin'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserBankAccountUpdateView.as_view(), name='profile' ),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
]