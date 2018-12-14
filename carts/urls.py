from django.conf.urls import url

from carts import views

urlpatterns = [
    url(r'^cart/$', views.carts, name='cart'),
    # 加入购物车
    url(r'^add_cart/$', views.add_cart, name='add_cart'),
    # 计算购物车中添加商品数量
    url(r'^count_cart/$', views.count_cart, name='count_cart'),
    # 修改购物车中的商品的勾选状态和商品数量
    url(r'^change_cart/$', views.change_cart, name='change_cart'),
    # 删除购物车中的商品
    url(r'^del_cart/(\d+)/$', views.del_cart, name='del_cart'),
    url(r'^is_select_cart/$', views.is_select_cart, name='is_select_cart')
]