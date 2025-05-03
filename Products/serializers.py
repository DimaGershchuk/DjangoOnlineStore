from rest_framework import serializers
from .models import Category, Brand, Product, Review


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializers(serializers.ModelSerializer):
    category = CategorySerializers()
    brand = BrandSerializers()
    thumbnail_url = serializers.ImageField(source='image_thumbnail', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'available', 'image', 'thumbnail_url', 'average_rating',
            'category', 'brand', 'created'
        ]

    def create(self, validated_data):
        # 1. Витягуємо вкладені дані для категорії з провалідованого словника
        category_data = validated_data.pop('category')
        # 2. Витягуємо вкладені дані для бренда з провалідованого словника
        brand_data = validated_data.pop('brand')

        # 3. Пошук або створення об’єкта Category:
        #    get_or_create(**category_data) спробує знайти Category
        #    з полями, які передали в category_data (наприклад, name/slug);
        #    якщо не знайде — створить новий. Повертає кортеж (instance, created_flag).
        category, _ = Category.objects.get_or_create(**category_data)

        # 4. Аналогічно для Brand:
        brand, _ = Brand.objects.get_or_create(**brand_data)

        # 5. Створення власне Product:
        #    Ми передаємо в нього вже отримані (або щойно створені) category і brand,
        #    а також усі інші поля, що залишилися у validated_data
        #    (наприклад name, price, stock, description тощо).
        product = Product.objects.create(category=category, brand=brand, **validated_data)

        # 6. Повертаємо створений екземпляр Product
        return product

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            cat_data = validated_data.pop('category')
            category, _ = Category.objects.get_or_create(**cat_data)
            instance.category = category
        if 'brand' in validated_data:
            br_data = validated_data.pop('brand')
            brand, _ = Brand.objects.get_or_create(**br_data)
            instance.brand = brand
        return super().update(instance, validated_data)


class ReviewSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at', 'product']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
