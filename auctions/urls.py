from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:auctionId>", views.listing, name="listing"),
    path("addWishlist/<int:auctionId>", views.addWishlist, name="addWishlist"),
    path("wishlist", views.wishlist, name="wishlist")
]
