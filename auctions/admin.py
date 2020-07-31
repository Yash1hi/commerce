from django.contrib import admin

from .models import Listing, Bid, Comment, User

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchers",)

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User)