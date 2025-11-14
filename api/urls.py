from django.urls import path
from .views import *

urlpatterns = [
    path("", PostListCreateApiView.as_view()),
    path("<int:pk>", PostRetriveUpdateDeleteView.as_view()),
]
