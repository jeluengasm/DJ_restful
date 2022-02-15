from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend # Create some filters for the API

from .serializers import ProductSerializer
from .models import Product

class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)
    
    def get_queryset(self):
        
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()
        else:
            queryset = Product.objects.all()
            if on_sale.lower() == 'true'
    