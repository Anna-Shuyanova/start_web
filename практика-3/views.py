from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from reviews.models import Doctor, Review
from .serializers import DoctorSerializer, ReviewSerializer

@api_view(['GET', 'POST'])
def doctor_list_create(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DoctorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'GET':
        serializer = DoctorSerializer(doctor, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = DoctorSerializer(doctor, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_list_create(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'GET':
        serializer = ReviewSerializer(review, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if review.author != request.user:
            return Response(
                {'error': 'Вы можете редактировать только свои отзывы'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ReviewSerializer(review, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if review.author != request.user:
            return Response(
                {'error': 'Вы можете удалять только свои отзывы'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)