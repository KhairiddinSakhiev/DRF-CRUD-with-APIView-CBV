from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializer import PostSerializer



class PostListCreateApiView(APIView):
    def get(self, request):
        posts = Post.objects.all()
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
        
