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
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

# from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import SmsCodeViewSet, UserRegViewset
from user_operation.views import UserFavViewset

router = DefaultRouter()
# 注册商品相关的url
router.register('goods', GoodsListViewSet, base_name='goods')
# 注册商品类别的url
router.register('categorys', CategoryViewSet, base_name='categorys')
# 手机验证码code
router.register('codes', SmsCodeViewSet, base_name='codes')

router.register('users', UserRegViewset, base_name='users')

router.register('userfavs', UserFavViewset, base_name='userfavs')

urlpatterns = [
	path('xadmin/', xadmin.site.urls),

	path('api-auth', include('rest_framework.urls', namespace='rest_framework')),

	# 商品列表页
	# path('goods/', GoodsListView.as_view(), name='goods-list'),
	path('', include(router.urls)),

	path('docs/', include_docs_urls(title='mx文档')),
	# drf自带的token,根据传入的user生成token,会保存到数据库中
	path('api-token-auth/', views.obtain_auth_token),

	# jwt的token验证方式
	path('jwt-auth/', obtain_jwt_token),
]
# django2.0 配置图片访问
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
