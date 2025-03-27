from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    """CRUD для продуктов с поиском"""
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    """CRUD для складов с фильтрацией по продукту"""
    queryset = Stock.objects.all().order_by("id")
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description']

    # при необходимости добавьте параметры фильтрации
