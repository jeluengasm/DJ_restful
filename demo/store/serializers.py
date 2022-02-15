from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """ Serialize the class Product """
    class Meta:
        """ Metaclass to setup the serializer """
        # Set the model object to serialize
        model = Product
        # Set the fields to display respect the model (attr)
        fields = ('id', 'name', 'description', 'price', 'sale_start', 'sale_end') 
        
    def to_representation(self, instance):
        """ Overrride the serialize representation and add extra fields. """
        data = super().to_representation(instance)
        data['is_on_sale'] = instance.is_on_sale()
        data['current_price'] = instance.current_price()
        
        return data