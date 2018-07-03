"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
import xadmin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

# from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet

router = DefaultRouter()
# 注册商品相关的url
router.register('goods', GoodsListViewSet, base_name='goods')

urlpatterns = [
	path('xadmin/', xadmin.site.urls),

	path('api-auth', include('rest_framework.urls', namespace='rest_framework')),

	# 商品列表页
	# path('goods/', GoodsListView.as_view(), name='goods-list'),
	path('', include(router.urls)),

	path('docs/', include_docs_urls(title='mx文档')),
]
# django2.0 配置图片访问
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
