from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from.models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
	# 获取去当前用户
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault()
	)

	class Meta:
		model = UserFav
		# 校验用户是否已经收藏过该商品,通过联合主键,用法同model中的unique_together = ("user", "goods")
		validators = [
			UniqueTogetherValidator(
				queryset=UserFav.objects.all(),
				fields=('user', 'goods'),
				message='该商品已经收藏'
			)
		]
		# 指定序列化字段
		fields = ('user', 'goods', 'id')
