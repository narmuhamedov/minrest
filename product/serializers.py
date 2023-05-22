from rest_framework import serializers
from product.models import Product, Category, Review
from rest_framework.exceptions import ValidationError
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    #category = CategorySerializer
    #reviews = ReviewSerializer(many=True)
    class Meta:
        model = Product
        #fields = "__all__"
        fields = "id title price category reviews rating count_reviews all_reviews".split()

    def get_category(self, product):
        try:
            return product.category.name
        except:
            return 'у данного товара нет категории'

    def get_reviews(self, product):
        #serializer = ReviewSerializer(product.reviews.all(), many=True)
        serializer = ReviewSerializer(Review.objects.filter(author__isnull=False,
                                                            product=product), many=True)
        return serializer.data

class ProductCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=10, min_length=2)
    description = serializers.CharField()
    price = serializers.FloatField()
    category_id = serializers.IntegerField()

    def validate(self, attrs):
        id = attrs['category_id']
        try:
            Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise ValidationError(f'Category with id={id}, not found')
        return attrs
