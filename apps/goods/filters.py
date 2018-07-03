import django_filters
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
	"""
	商品的过滤类
	"""
	price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')  # 大于等于
	price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
	'''
	不加lookup表示精确匹配, i表示忽略大小写,模糊查询
	'''
	name = django_filters.CharFilter(name='name', lookup_expr='icontains')

	class Meta:
		model = Goods
		fields = ['price_min', 'price_max', 'name']
