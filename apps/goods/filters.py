import django_filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
	"""
	商品的过滤类
	"""
	pricemin = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')  # 大于等于
	pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
	'''
	不加lookup表示精确匹配, i表示忽略大小写,模糊查询
	'''
	name = django_filters.CharFilter(name='name', lookup_expr='icontains')
	# 自定义方法进行过滤
	top_category = django_filters.NumberFilter(method='top_category_filter')

	def top_category_filter(self, queryset, name, value):
		# 根据类别过滤
		return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
			category__parent_category__parent_category_id=value))

	class Meta:
		model = Goods
		fields = ['pricemin', 'pricemax', 'name']
