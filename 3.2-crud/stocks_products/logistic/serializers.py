from rest_framework import serializers
from decimal import Decimal
from logistic.models import Product, Stock, StockProduct
class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов"""

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    """Сериализатор для позиций товаров на складе"""
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.01")) 
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

class StockSerializer(serializers.ModelSerializer):
    """Сериализатор для склада с позицией товаров"""
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        """Создание склада и связанных позиций товаров"""
        positions_data = validated_data.pop('positions')  # Извлекаем позиции
        stock = Stock.objects.create(**validated_data)  # Создаем склад

        # Заполняем связанные таблицы (StockProduct)
        for position in positions_data:
            StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        """Обновление склада и связанных позиций товаров"""
        positions_data = validated_data.pop('positions', [])

        # Обновляем данные самого склада
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        # Обновляем связанные продукты на складе
        for position in positions_data:
            stock_product, created = StockProduct.objects.update_or_create(
                stock=instance,
                product=position['product'],
                defaults={
                    'quantity': position['quantity'],
                    'price': position['price']
                }
            )

        return instance
