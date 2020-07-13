from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms


from .models import User, Auctions, Bids, Comments, Wishlists

category_choices = [
    ('Arts', 'Arts, Crafts and Sewing'),
    ('Cars', 'Automotive parts'),
    ('Gene', 'General'),
    ('Toys', 'Toys')
    ]

class NewListing(forms.Form):
    name = forms.CharField(label="Name", max_length=64)
    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=2)
    description = forms.CharField(label = "description", max_length=500)
    category = forms.ChoiceField(choices=category_choices, required=True)
    image = forms.URLField(required=False)


@login_required(login_url="/login", redirect_field_name='')
def index(request):
    auctions = Auctions.objects.all()
    return render(request, "auctions/index.html", {
        "auctions":auctions
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login", redirect_field_name='')
def create(request):
    user = request.user
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            bid = Auctions()
            bid.name = form.cleaned_data["name"]
            bid.price = form.cleaned_data["price"]
            bid.description = form.cleaned_data["description"]
            bid.category = form.cleaned_data["category"]
            bid.user = user
            bid.image = form.cleaned_data["image"]
            bid.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form":NewListing
            })

    return render(request,"auctions/create.html", {
        "form":NewListing()
    })

def listing(request, auctionId):
    user = request.user
    if Auctions.objects.get(pk=auctionId) is None:
        return render(request, "auctions/error.html", {
            "message":"Listing does not exit."
        })
    auction = Auctions.objects.get(pk=auctionId)
    creater = user == auction.user

    try:
        wishlist = Wishlists.objects.get(user=user, item = auction) is not None
    except Wishlists.DoesNotExist:
        wishlist = False

    return render(request, "auctions/listing.html", {
        "auction":auction,
        "creater": creater,
        "wishlist": wishlist
    })

def addWishlist(request, auctionId):
    user = request.user
    if Auctions.objects.get(pk=auctionId) is None:
        return render(request, "auctions/error.html", {
            "message":"Listing does not exit."
        })
    
    auction = Auctions.objects.get(pk=auctionId)
    
    try:
        exist = Wishlists.objects.get(user=user, item = auction)
    except Wishlists.DoesNotExist:    
        wishlist = Wishlists()
        wishlist.user = user
        wishlist.item = auction
        wishlist.save()
        return HttpResponseRedirect(reverse("listing", args=(auctionId,)))
    
    
    return render(request, "auctions/error.html", {
            "message":"Added to wishlist already."
        })

    

@login_required(login_url="/login", redirect_field_name='')
def wishlist(request):
    user = request.user
    wishlists = Wishlists.objects.filter(user = user)
    return render(request, "auctions/wishlist.html", {
        "wishlists":wishlists
    })
