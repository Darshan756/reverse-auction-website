from rest_framework import serializers
from .models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserAccount
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        if 'user_type' in validated_data and instance.user_type != validated_data['user_type']:
            raise serializers.ValidationError({"user_type": "Cannot change user type"})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
