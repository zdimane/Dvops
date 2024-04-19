from django.urls import path, re_path
from . import views

urlpatterns = [
    path("index", views.Index.as_view()  , name="index"),
    path("", views.Main.as_view()  , name="main"),
    path("signup", views.Signup.as_view() , name="signup"),
    path("login", views.Login.as_view() , name="login"),
    path("logout", views.logout, name="logout"),
    path("cart", views.Cart.as_view(), name="cart"),
    path("check-out", views.CheckOut.as_view(), name="checkout"),
    path("orders", views.OrderView.as_view(), name="orders"),
    path("forgotpass", views.Forgotpass.as_view(), name="forgotpass"),
    path("otp", views.Otp.as_view(), name="otp"),
    path("ordermanage", views.Ordermanage.as_view(), name="ordermanage"),
    path("profile", views.Profile.as_view(), name="profile"),
    path("products", views.Products.as_view(), name="products"),
]