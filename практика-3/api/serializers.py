from rest_framework import serializers
from reviews.models import Doctor, Review
from django.db.models import Avg

class DoctorSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(source='reviews.count', read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'specialty', 'created_at', 
                 'review_count', 'average_rating']
    
    def get_average_rating(self, obj):
        agg = obj.reviews.aggregate(avg=Avg('rating'))
        return agg['avg'] if agg['avg'] is not None else 0

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    
    class Meta:
        model = Review
        fields = ['id', 'doctor', 'author', 'text', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)