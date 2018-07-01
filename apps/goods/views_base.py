from django.views.generic.base import View

from goods.models import Goods


class GoodsListView(View):
	def get(self, request):
		"""
		通过django的view实现商品列表页
		:param request:
		:return:
		"""
		json_list = []
		goods = Goods.objects.all()[:10]
		# 1.自己定义实体-json转换
		# for good in goods:
		# 	json_dict = {}
		# 	json_dict['name'] = good.name
		# 	json_dict['category'] = good.category.name
		# 	json_dict['market_price'] = good.market_price
		# 	json_list.append(json_dict)

		# 2.通过django的model_to_dict进行json转换
		# ImageFieldFile 等特殊字段无法进行转化
		# from django.forms.models import model_to_dict
		# for good in goods:
		# 	json_dict = model_to_dict(good)
		# 	json_list.append(json_dict)
		#
		# import json
		# from django.http import HttpResponse
		# return HttpResponse(json.dumps(json_list), content_type='application/json')

		# 3.通过django的serializers序列化方法进行转化
		import json
		from django.core import serializers
		json_data = serializers.serialize('json', goods)
		json_data = json.loads(json_data)
		from django.http import JsonResponse
		return JsonResponse(json_data, safe=False)
