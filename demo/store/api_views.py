from django.utils import timezone
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend # Create some filters for the API (according to the attributes selected from the view)
from rest_framework.filters import SearchFilter # Create a search filter (based on substrings, according to the attributes selected from the view)
from rest_framework.pagination import LimitOffsetPagination # Allows the pagination of the view


from .serializers import ProductSerializer
from .models import Product

class ProductsPagination(LimitOffsetPagination):
    """ Pagination class, with internal properties
        See documentation in: https://www.django-rest-framework.org/api-guide/pagination/
    """
    default_limit = 3 
    max_limit = 100


class ProductList(ListAPIView): # Extends from ListAPIView (only GET request)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter) # Integrate DjangoFilterBackend, SearchFilter as the filters of the API
    filter_fields = ('id',)
    search_fields = ('name', 'description') # Search fields from Product model 
    pagination_class = ProductsPagination
    
    def get_queryset(self):
        
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()
        else:
            queryset = Product.objects.all()
            if on_sale.lower() == 'true':
                now = timezone.now()
                return queryset.filter(
                    sale_start__lte = now,
                    # sale_end__gte = now,
                )
            return queryset