from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from random import choice

from .serializers import SmsSerializer, UserRegSerializer
from .models import VerifyCode
from utils.sendMsg import SendMsg

User = get_user_model()


class CustomBackend(ModelBackend):
	"""
	自定义用户验证
	"""

	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			user = User.objects.get(Q(username=username) | Q(mobile=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
	"""
	发送短信验证码
	"""
	serializer_class = SmsSerializer

	def generate_code(self):
		"""
		生成四位code
		:return:
		"""
		seeds = '1234567890'
		random_str = []
		for i in range(4):
			random_str.append(choice(seeds))

		return ''.join(random_str)

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		# 获取手机号码
		mobile = serializer.validated_data['mobile']
		# 发送短信
		code = self.generate_code()
		send_msg = SendMsg(api_key='')
		res = send_msg.seng_msg(code=code, mobile=mobile)
		if res:
			verify_code = VerifyCode(code=code, mobile=mobile)
			verify_code.save()


class UserRegViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
	"""
	用户
	"""
	serializer_class = UserRegSerializer
	queryset = User.objects.all()

	'''
	注册完自动完成登录功能,需重写create和生成jwt的token
	'''
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = self.perform_create(serializer)
		# 生成jwt的token并返回
		res_dict = serializer.data
		payload = jwt_payload_handler(user)
		res_dict['token'] = jwt_encode_handler(payload)
		res_dict['name'] = user.name if user.name else user.username
		headers = self.get_success_headers(serializer.data)
		return Response(res_dict, status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		return serializer.save()
