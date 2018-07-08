from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from .serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
	"""
	用户收藏功能
	"""
	# queryset = UserFav.objects.all()
	# IsAuthenticated 校验是否登录
	# IsOwnerOrReadOnly 校验是否有操作权限
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
	serializer_class = UserFavSerializer
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)  # 局部接口配置token验证,与settings中的全局相对应

	def get_queryset(self):
		return UserFav.objects.filter(self.request.user)
