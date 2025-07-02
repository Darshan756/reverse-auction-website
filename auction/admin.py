from django.contrib import admin
from .models import Category,SubCategory,BidRequest,Bid,AuctionResult
# Register your models here.

admin.site.register(Category)

admin.site.register(SubCategory)

admin.site.register(BidRequest)

admin.site.register(Bid)

admin.site.register(AuctionResult)