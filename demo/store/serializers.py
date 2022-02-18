from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """ Serialize the class Product """
    
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)
    class Meta:
        """ Metaclass to setup the serializer """
        # Set the model object to serialize
        model = Product
        # Set the fields to display respect the model (attr)
        fields = (
            'id', 'name', 'description', 'price', 'sale_start', 'sale_end',
            'is_on_sale', 'current_price', 
            ) 
        
    # def to_representation(self, instance):
    #     """ Overrride the serialize representation and add extra fields. """
    #     data = super().to_representation(instance)
    #     data['is_on_sale'] = instance.is_on_sale()
    #     data['current_price'] = instance.current_price()
        
    #     return data