from django.db import models
from user_accounts.models import UserAccount
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(max_length=250,blank=True,null=True,verbose_name="Category Name" )
    
    
    def __str__(self):
        return self.cat_name 
    


class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category")
    sub_name = models.CharField(max_length=250,blank=True,null=True)
    def __str__(self):
        return f"{self.category.cat_name}-{self.sub_name}"


def validate_image_size(image):
    max_img_mb = 5
    if image.size > max_img_mb * 1024 * 1024:
        raise ValidationError(f"Image size should not exceed {max_img_mb} MB.")

class BidRequest(models.Model):
    buyer = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name="buyer" ,limit_choices_to={'user_type':'buyer'})
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    sub_category = models.ForeignKey(SubCategory,on_delete=models.SET_NULL,null=True)

    title =  models.CharField(max_length=250)
    description = models.TextField()
    document = models.FileField(upload_to='bid_request_documents/')
    related_image = models.ImageField(upload_to='bid_request_related_images/',validators=[validate_image_size])
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50,help_text="e.g., pieces, kg, liters")
  
    

    location = models.CharField(max_length=255)
    delivery_deadline = models.DateField()

    budget = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    
  
    created_at = models.DateTimeField(auto_now_add=True)
    open_date = models.DateTimeField()
    close_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    is_awarded = models.BooleanField(default=False)

    def __str__(self):
        return F"{self.title}  {self.description} {self.buyer.full_name} - {self.buyer.phone_number}"
    

class Bid(models.Model):
    vendor = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name="supplier",limit_choices_to={"user_type":"vendor"})
    bid_request = models.ForeignKey(BidRequest,on_delete=models.CASCADE,related_name='rfqs')
    
    bid_amount = models.DecimalField(max_digits=12,decimal_places=2)
    bid_description = models.TextField(blank=True , null=True)
    delivery_days = models.PositiveIntegerField(help_text="Delivery time in days")
    related_documents = models.FileField(upload_to='bid_related_documents/',null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_selected = models.BooleanField(default=False)

    class Meta:
        unique_together = ['vendor','bid_request']
    
    def __str__(self):
        return f"{self.vendor.full_name} - {self.vendor.company_name} - ₹{self.bid_amount} - {self.bid_description} -  "
    

class AuctionResult(models.Model):
    bid_request = models.OneToOneField(BidRequest,on_delete=models.CASCADE,related_name='result')
    winning_bid = models.OneToOneField(Bid, on_delete=models.SET_NULL, null=True,blank=True,related_name='won_auction')

    awarded_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"Auction Result for {self.bid_request.title} - won by {self.winning_bid.bid_amount if self.winning_bid else 'N/A'}"

    
    

