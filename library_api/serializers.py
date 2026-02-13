from rest_framework import serializers
from .models import Room, Shelf, Book, Student, Borrow, RevisionPaper
from django.contrib.auth.models import User


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'form', 'stream', 'class_teacher', 'total_students']


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = [
            'id', 'shelf_name', 'shelf_code', 'category',
            'form_class', 'shelf_count', 'max_borrow_per_student'
        ]


class BookSerializer(serializers.ModelSerializer):
    shelf = serializers.PrimaryKeyRelatedField(queryset=Shelf.objects.all())
    category = serializers.CharField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'publishers', 'first_publication', 'ISBN',
            'book_number', 'shelf', 'category', 'book_picture', 'created'
        ]


class StudentSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    student_id = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'admission_number', 'student_id',
            'year_of_study', 'current_class', 'room', 'student_picture', 'created'
        ]


class BorrowSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    shelf = serializers.PrimaryKeyRelatedField(read_only=True)
    processed_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Borrow
        fields = [
            'id', 'book', 'student', 'borrowed_date', 'due_date', 'returned',
            'returned_date', 'processed_by', 'shelf'
        ]

    def create(self, validated_data):
        book = validated_data['book']
        validated_data['shelf'] = book.shelf
        validated_data['processed_by'] = self.context['request'].user
        return super().create(validated_data)


class RevisionPaperSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RevisionPaper
        fields = [
            'id', 'title', 'room', 'subject', 'file',
            'uploaded_by', 'uploaded_at'
        ]

    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)
