from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Post
from .serializer import PostSerializer
from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from .permissions import *

from drf_yasg.utils import swagger_auto_schema



class PostListCreateApiView(generics.GenericAPIView):
    serializer_class = PostSerializer
    
    @swagger_auto_schema(tags=["Posts"])
    def get(self, request):
        posts = Post.objects.all().order_by("-id")
        title = request.query_params.get("t", None)
        if title:
            posts = posts.filter(title=title)
        date_obj = request.query_params.get("d", None)
        print("test", date_obj)
        if date_obj:
            filter_date = datetime.strptime(date_obj, "%Y-%m-%d")
            print(filter_date)
            posts = posts.filter(created_at__year=filter_date.year, created_at__month=filter_date.month, created_at__day=filter_date.day)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Posts"])
    def post(self, request):
        
        if serializer.is_valid():
            serializer = self.serializer_class(data = request.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetriveUpdateDeleteView(generics.GenericAPIView):
    def get(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        if post:
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Post not found!"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        if post:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Post not found!"}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        if post:
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Post not found!"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        if post:
            try:
                post.delete()
                return Response({"message":"Post deleted!"}, status=status.HTTP_204_NO_CONTENT)
            except Exception as er:
                return Response({"error": str(er)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Post not found!"}, status=status.HTTP_400_BAD_REQUEST)
        


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDestroyAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

class PostCreateListGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get("title", None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    def get_serializer_class(self):
        return super().get_serializer_class()


class PostRetriveUpdateDeleteGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    


class PostAPIView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [CanPublish]


