from rest_framework import serializers

from.models import Goods, GoodsCategory, GoodsImage

"""
class GoodsSerializer(serializers.Serializer):
	name = serializers.CharField(required=True, max_length=100)
	click_num = serializers.IntegerField(default=0)
	goods_front_image = serializers.ImageField()  # 会从settings配置文件中拿到媒体文件的前缀路径加上
	等同 ModelSerializer的用法
"""


class GoodsCategorySerializer3(serializers.ModelSerializer):
	# 通过Model中定义的sub_cat来实现关联的子级数据
	class Meta:
		model = GoodsCategory
		fields = '__all__'


class GoodsCategorySerializer2(serializers.ModelSerializer):
	# 通过Model中定义的sub_cat来实现关联的子级数据
	sub_cat = GoodsCategorySerializer3(many=True)

	class Meta:
		model = GoodsCategory
		fields = '__all__'


class GoodsCategorySerializer(serializers.ModelSerializer):
	# 通过Model中定义的sub_cat来实现关联的子级数据
	sub_cat = GoodsCategorySerializer2(many=True)

	class Meta:
		model = GoodsCategory
		fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = GoodsImage
		fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
	# 关联字段对象的序列化
	category = GoodsCategorySerializer()
	images = GoodsImageSerializer(many=True)

	class Meta:
		model = Goods
		# 指定序列化字段
		# fields = ('name', 'click_num', 'market_price', 'add_time')
		fields = '__all__'
