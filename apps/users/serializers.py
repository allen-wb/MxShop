from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model
import re
from datetime import datetime, timedelta
from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
	mobile = serializers.CharField(max_length=11)

	def validate_mobile(self, mobile):
		"""
		校验手机号码
		:param mobile:
		:return:
		"""
		# 验证手机号码是否合法
		if not re.match(REGEX_MOBILE, mobile):
			raise serializers.ValidationError('手机号码非法')

		# 验证上次发送时间
		one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
		if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
			raise serializers.ValidationError('距离上一次发送未超过60秒')

		# 手机是否已注册
		user = User.objects.filter(mobile=mobile)
		if user.count():
			raise serializers.ValidationError('该手机号码已存在')

		return mobile


class UserRegSerializer(serializers.ModelSerializer):
	"""
	用户注册校验
	"""
	'''
	code的write_only属性
	Set this to True to ensure that the field may be used when updating or creating an instance, 
	but is not included when serializing the representation.
	Defaults to False
	'''
	code = serializers.CharField(required=True, max_length=4, min_length=4, write_only=True, label='验证码')
	# drf自带的validators进行校验
	name = serializers.CharField(required=True, allow_blank=False, label='用户名',
								 validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')])
	password = serializers.CharField(style={'input_type': 'password'}, label='密码', write_only=True)

	'''
	默认添加的密码是明文,没有经过加密,可以通过重写create方法来实现,或者通过信号量来实现,见signals文件
	'''
	# def create(self, validated_data):
	# 	user = super(UserRegSerializer, self).create(validated_data=validated_data)
	# 	# 对密码进行加密
	# 	user.set_password(validated_data['password'])
	# 	user.save()
	# 	return user

	def validated_code(self, code):
		# 前端传过来的数据都会存在initial_data中
		verify_codes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
		if verify_codes:
			last_code = verify_codes[0]
			five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
			if five_minute_ago > last_code.add_time:
				raise serializers.ValidationError('验证码过期')

			if last_code.code != code:
				raise serializers.ValidationError('验证码错误')

		else:
			raise serializers.ValidationError('验证码错误')

	def validate(self, attrs):
		attrs['mobile'] = attrs['username']
		del attrs['code']
		return attrs

	class Meta:
		model = User
		fields = ('username', 'code', 'mobile', 'password')
