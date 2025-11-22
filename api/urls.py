from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("", PostAPIView, basename="posts")


urlpatterns = [
    path("posts/", PostListCreateApiView.as_view()),
    path("posts/<int:pk>", PostRetriveUpdateDeleteView.as_view()),
    
    
    path("", PostListAPIView.as_view()),
    path("detail/<int:pk>", PostDetailAPIView.as_view()),
    path("edit/<int:pk>", PostUpdateAPIView.as_view()),
    path("delete/<int:pk>", PostDestroyAPIView.as_view()),
    path("create", PostCreateAPIView.as_view()),
    
    
    path("post", PostCreateListGenericAPIView.as_view()),
    path("post/<int:pk>", PostRetriveUpdateDeleteGenericAPIView.as_view()),
    
    path("test", include(router.urls)),
]
