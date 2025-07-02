from rest_framework import serializers 
from .models import BidRequest ,Bid,validate_image_size
from datetime import date
from user_accounts.serializers import BuyerSerializer

class BidRequestSerializer(serializers.ModelSerializer):
    
    buyer = BuyerSerializer()
    class Meta:
        model = BidRequest
        fields = '__all__'

    def validate_related_image(self,image):
        validate_image_size(image)
        return image
    
    def validate_delivery_deadline(self,delivery_date):
        if delivery_date < date.today():
            raise serializers.ValidationError('Delivery deadline cannot be in the past.')
        return delivery_date
    def validate(self, data):
        delivery_deadline = data.get('delivery_deadline')
        open_date = data.get('open_date')

        if delivery_deadline and open_date:
            if open_date > delivery_deadline:
                raise serializers.ValidationError("Open date cannot be after the delivery deadline.")

        return data  


class BidSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bid
        fields = '__all__'
    
    def validate_bid_amount(self,value):
        if value <= 0 :
            raise serializers.ValidationError('Bid amount should be greater than 0')
        return value 
    

    def validate(self, data):
        bid_amount = data.get('bid_amount')
        bid_request = data.get('bid_request')

        if bid_amount and bid_request and bid_request.budget:
            if bid_amount > bid_request.budget:
                raise serializers.ValidationError("Bid amount cannot exceed the buyer's budget.")
        
            lowest_bid = Bid.objects.filter(bid_request = bid_request).order_by('bid_amount').first()
            if lowest_bid and bid_amount > lowest_bid.bid_amount:
               raise serializers.ValidationError('')

        
        return data