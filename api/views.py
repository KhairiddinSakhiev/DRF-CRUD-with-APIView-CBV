from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializer import PostSerializer
from datetime import datetime



class PostListCreateApiView(APIView):
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
    
    def post(self, request):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetriveUpdateDeleteView(APIView):
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
        
