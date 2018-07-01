from rest_framework import serializers

from.models import Goods, GoodsCategory

"""
class GoodsSerializer(serializers.Serializer):
	name = serializers.CharField(required=True, max_length=100)
	click_num = serializers.IntegerField(default=0)
	goods_front_image = serializers.ImageField()  # 会从settings配置文件中拿到媒体文件的前缀路径加上
	等同 ModelSerializer的用法
"""


class GoodsCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = GoodsCategory
		fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
	# 关联字段对象的序列化
	category = GoodsCategorySerializer()

	class Meta:
		model = Goods
		# 指定序列化字段
		# fields = ('name', 'click_num', 'market_price', 'add_time')
		fields = '__all__'
