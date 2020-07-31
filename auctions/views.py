from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "user": request.user,
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

@login_required
def watchlist(request):
    logUser = request.user
    return render(request, "auctions/watchlist.html", {
        "watching": logUser.watchers.all(),
        "user": request.user.username
    })
    
@login_required
def createPage(request):
    if request.method == "POST":
        item = request.POST["item"]
        category = request.POST["category"]
        description = request.POST["description"]
        image = request.POST["image"]
        startBid = request.POST["startBid"]
        newItem = Listing(name=item, category=category, description=description, image=image, createdBy=request.user)
        newItem.save()
        startBid = Bid(listing_id=newItem, bid=float(startBid), bidder=request.user)
        startBid.save()
        return HttpResponseRedirect("/")
    else:
        categoryList, item_ids = [], []
        for item in Listing.objects.all():
            if item.category not in item_ids:
                categoryList.append(item)
                item_ids.append(item.category)
        return render(request, "auctions/createPage.html", {
        "listings": Listing.objects.all(),
        "catList":categoryList
        })

def itemPage(request, itemName):
    item = Listing.objects.get(name=itemName)
    bidList = Bid.objects.filter(listing_id=item).order_by('bid')
    highestBid = bidList[len(bidList)-1] 
    return render(request, "auctions/itemPage.html", {
        "itemListing": item,
        "itemBids": item.Bids.all(),
        "itemComments": item.Comments.all(), 
        "highBid": highestBid,
    })

@login_required
def createComment(request, itemName):
    if request.method == "POST":
        comment = request.POST["comment"]
        listName = Listing.objects.get(name=itemName)
        newComment = Comment(listing_id=listName, user=request.user, comment=comment, date=datetime.now())
        newComment.save()
        return HttpResponseRedirect("/"+itemName)
    else:
        return render(request, "auctions/createComment.html", {
        "itemName":itemName
    })

@login_required
def createBid(request, itemName):
    if request.method == "POST":
        listName = Listing.objects.get(name=itemName)
        bidList = Bid.objects.filter(listing_id=listName).order_by('bid')
        highestBid = bidList[len(bidList)-1] 
        bid = float(request.POST["bid"])
        if float(highestBid.bid) < bid: 
            newBid = Bid(listing_id=listName, bidder=request.user, bid=bid)
            newBid.save()
            return HttpResponseRedirect("/"+itemName)
        else:
            return render(request, "auctions/createBid.html", {
                "itemName":itemName,
                "message":"Please enter a bid higher than the current highest. The current highest bid is " + str(highestBid.bid)
            })
    else:
        return render(request, "auctions/createBid.html", {
        "itemName":itemName
    })

@login_required
def watch(request, itemName):
    item = Listing.objects.get(name=itemName)
    item.watchers.add(request.user)
    return HttpResponseRedirect("/")

@login_required
def removeWatch(request, itemName):
    item = Listing.objects.get(name=itemName)
    item.watchers.remove(request.user)
    return HttpResponseRedirect("/watchlist")

def categories(request):
    categoryList, item_ids = [], []
    for item in Listing.objects.all():
        if item.category not in item_ids:
            categoryList.append(item)
            item_ids.append(item.category)
    return render(request, "auctions/categories.html", {
        "categoryList":categoryList,
    })

def categoryPage(request, catName):
    items=Listing.objects.filter(category=catName)
    return render(request, "auctions/categoryPage.html", {
        "listings":items,
        "category": catName
    })

@login_required
def end(request, itemName):
    removeItem = Listing.objects.get(name=itemName)
    removeItem.delete()
    return HttpResponseRedirect("/")
    