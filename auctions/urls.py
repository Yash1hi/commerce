from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createPage", views.createPage, name="createPage"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:catName>", views.categoryPage, name="categoryPage"),
    path("<str:itemName>/end", views.end, name="end"),
    path("<str:itemName>/newComment", views.createComment, name="createComment"),
    path("<str:itemName>/addWatch", views.watch, name="watch"),
    path("<str:itemName>/removeWatch", views.removeWatch, name="removeWatch"),
    path("<str:itemName>/newBid", views.createBid, name="createBid"),
    path("<str:itemName>", views.itemPage, name="itemPage")
]
