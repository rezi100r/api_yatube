from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token)
]
