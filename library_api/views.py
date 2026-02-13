
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Room, Shelf, Book, Student, Borrow, RevisionPaper
from .serializers import (
    RoomSerializer, ShelfSerializer, BookSerializer,
    StudentSerializer, BorrowSerializer, RevisionPaperSerializer
)


class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarian()]
        return super().get_permissions()


class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarian()]
        return super().get_permissions()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarian()]
        return super().get_permissions()


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarian()]
        return super().get_permissions()


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'return_book']:
            return [IsLibrarian()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        book = Book.objects.get(pk=request.data['book'])
        student = Student.objects.get(pk=request.data['student'])
        borrowed_count = Borrow.objects.filter(
            student=student,
            shelf=book.shelf,
            returned=False
        ).count()
        if borrowed_count >= book.shelf.max_borrow_per_student:
            return Response({
                'error': f"Borrowing limit reached for shelf '{book.shelf.shelf_name}'."
            }, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['put'], url_path='return')
    def return_book(self, request, pk=None):
        borrow = self.get_object()
        if not borrow.returned:
            borrow.returned = True
            borrow.returned_date = timezone.now()
            borrow.save()
            borrow.shelf.shelf_count = borrow.shelf.books.count()
            borrow.shelf.save(update_fields=['shelf_count'])
            return Response({'status': 'Book returned'}, status=status.HTTP_200_OK)
        return Response(
            {'error': 'Book already returned'},
            status=status.HTTP_400_BAD_REQUEST
        )


class RevisionPaperViewSet(viewsets.ModelViewSet):
    queryset = RevisionPaper.objects.all()
    serializer_class = RevisionPaperSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarian()]
        return super().get_permissions()
