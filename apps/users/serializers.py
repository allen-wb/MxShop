from rest_framework import serializers

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
