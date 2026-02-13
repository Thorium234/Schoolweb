from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'shelves', views.ShelfViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'borrows', views.BorrowViewSet)
router.register(r'revision-papers', views.RevisionPaperViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', obtain_auth_token, name='token_auth'),
]