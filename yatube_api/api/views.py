from django.shortcuts import get_object_or_404
from posts.models import Post, Group, Comment
from rest_framework import viewsets, permissions

from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение позволяющее редактировать объект только владельцам.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет группы только для чтения"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментария"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        post_comments = Comment.objects.filter(post=post)
        return post_comments


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет поста"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
