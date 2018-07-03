from goods.serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets

from .models import Goods
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
	# 自定义分页信息,自定义分页配置信息之后,配置文件中的参数无效
	# page_size的默认信息会被页面传入的值覆盖
	page_size = 20
	page_size_query_param = 'page_size'
	page_query_param = 'p'  # 分页时查询的页码参数
	max_page_size = 1000


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer
	pagination_class = GoodsPagination
	filter_backends = (DjangoFilterBackend,)
	filter_class = GoodsFilter


# class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
# 	queryset = Goods.objects.all()
# 	serializer_class = GoodsSerializer
# 	pagination_class = GoodsPagination
#
# 	# 会覆盖掉上面的queryset,自定义查询过滤
# 	def get_queryset(self):
# 		# 从drf的request中获取请求参数
# 		price_min = self.request.query_params.get('price_min', 0)
# 		if price_min:
# 			self.queryset = Goods.objects.filter(shop_price__gt=int(price_min))
# 		return self.queryset

# class GoodsListView(generics.ListAPIView):
# 	queryset = Goods.objects.all()
# 	serializer_class = GoodsSerializer
# 	pagination_class = GoodsPagination

# 等同于调用下面的APIView
# class GoodsListView(APIView):
# 	"""
# 	List all goods
# 	"""
#
# 	def get(self, request, format=None):
# 		goods = Goods.objects.all()[:10]
# 		goods_serializer = GoodsSerializer(goods, many=True)
# 		return Response(goods_serializer.data)

# def post(self, request, format=None):
# 	serializer = GoodsSerializer(data=request.date)
# 	if serializer.is_valid():
# 		serializer.save()
# 		return Response(serializer.data, status=status.HTTP_201_CREATED)
# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
