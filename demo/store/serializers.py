from email.policy import default
from logging import PlaceHolder
from rest_framework import serializers
from .models import Product, ShoppingCartItem

class CartItemSerializer(serializers.ModelSerializer):
    """ Serializer of the model 'CartItemSerializer', who has a Foreign key
        with 'Product' model.
    """
    # Add integer fields
    quantity = serializers.IntegerField(min_value=1, max_value=100)
    
    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'quantity')
        
class ProductSerializer(serializers.ModelSerializer):
    """ Serialize the class Product """
    
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)
    cart_items = serializers.SerializerMethodField()
    # price = serializers.FloatField(min_value=1.0, max_value=100000.0)
    price = serializers.DecimalField(
        min_value=1.0, max_value=100000.0,
        max_digits=None, decimal_places=2,
        )
    sale_start = serializers.DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2019"',
        style={'input_type':'text', 'placeholder': '12:01 AM 28 July 2019'},
    )
    sale_end = serializers.DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2019"',
        style={'input_type':'text', 'placeholder': '12:01 AM 28 July 2019'},
    )
    
    photo = serializers.ImageField(default=None)
    warranty = serializers.FileField(write_only=True, default=None)
    
    class Meta:
        """ Metaclass to setup the serializer """
        # Set the model object to serialize
        model = Product
        # Set the fields to display respect the model (attr)
        fields = (
            'id', 'name', 'description', 'price', 'sale_start', 'sale_end',
            'is_on_sale', 'current_price', 'cart_items', 'photo', 'warranty', 
            ) 
    
    def get_cart_items(self, instance):
        """ Getter of 'cart_items' serializer method field. 
            Note: Getters of the serialized models must be written 'get_<name_of_serializerMethodField>' (cart_items in this case)"""
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data
    
    def update(self, instance, validated_data):
        if validated_data.get('warranty', None):
            instance.description += '\nWarranty information:\n'
            instance.description += b'; '.join(
                validated_data['warranty'].readlines()
            ).decode()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data.pop('warranty')
        return Product.objects.create(**validated_data)

class ProductStatSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
        )
    )

    # def to_representation(self, instance):
    #     """ Overrride the serialize representation and add extra fields. """
    #     data = super().to_representation(instance)
    #     data['is_on_sale'] = instance.is_on_sale()
    #     data['current_price'] = instance.current_price()
        
    #     return data