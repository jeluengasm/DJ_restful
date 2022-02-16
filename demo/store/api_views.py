from xml.dom import ValidationErr
from django.utils import timezone
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend # Create some filters for the API (according to the attributes selected from the view)
from rest_framework.filters import SearchFilter # Create a search filter (based on substrings, according to the attributes selected from the view)
from rest_framework.pagination import LimitOffsetPagination # Allows the pagination of the view
from rest_framework.exceptions import ValidationError # Exception handler to raise in ValidationError
from django.core.cache import cache


from .serializers import ProductSerializer
from .models import Product

class ProductsPagination(LimitOffsetPagination):
    """ Pagination class, with internal properties
        See documentation in: https://www.django-rest-framework.org/api-guide/pagination/
    """
    default_limit = 5 
    max_limit = 100


class ProductList(ListAPIView):
    """ Extends from ListAPIView (only GET request)
    See doc. in: https://www.django-rest-framework.org/api-guide/generic-views/#listapiview
    """
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
        

class ProductCreate(CreateAPIView):
    """ Used for create-only endpoints.
        Provides a POST method handler. Doc. in: https://www.django-rest-framework.org/api-guide/generic-views/#createapiview
    """
    serializer_class = ProductSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price is not None and float(price) <= 0.0:
                raise ValidationError({'price': 'Must be above $0.00.'})
        except ValueError:
            raise ValidationError({'price': 'A valid number is required.'})
        return super().create(request, *args, **kwargs)
        
class ProductDestroy(DestroyAPIView,ProductList):
    """ Used for delete-only endpoints.
        Provides a DELETE method handler. Doc. in: https://www.django-rest-framework.org/api-guide/generic-views/#destroyapiview
    """
    queryset = Product.objects.all()
    lookup_field = 'id'
    
    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        
        if response.status_code == 204: # 204 No Content response
            cache.delete(f"product_data_{product_id}")
        return response
