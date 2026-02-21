"""Serializers for products app."""
from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'image', 'is_active', 'children']
        read_only_fields = ['slug']

    def get_children(self, obj):
        return CategorySerializer(obj.children.filter(is_active=True), many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'compare_at_price',
            'sku', 'stock', 'category', 'category_name', 'image',
            'is_active', 'is_featured', 'weight',
            'in_stock', 'discount_percentage',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['slug']
