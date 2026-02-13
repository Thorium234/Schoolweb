from django.contrib import admin
from .models import Room, Shelf, Book, Student, Borrow, RevisionPaper

admin.site.register(Room)
admin.site.register(Shelf)
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Borrow)
admin.site.register(RevisionPaper)