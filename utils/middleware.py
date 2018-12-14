from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from carts.models import ShoppingCart
from user.models import User
import re

class LoginStatusMilddleware(MiddlewareMixin):

    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            request.user = user



        not_need_check = ['/user/login/',
                          '/user/register/',
                          '/goods/index/',
                          '/carts/cart/',
                          '/media/.*',
                          '/goods/detail/.*',
                          '/carts/add_cart/',
                          '/carts/count_cart/',
                          '/carts/change_cart/',
                          '/carts/del_cart/.*',
                          '/carts/is_select_cart/']
        for not_check in not_need_check:
            if re.match(not_check, request.path):
                return None
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect('/user/login/')

        user = User.objects.get(pk=user_id)
        if not user:
            return HttpResponseRedirect('/user/login/')
        request.user = user
        return None

    def process_response(self, request, response):
        return response


class SessionSyncMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # 没登录就不管数据同步
        # 登录情况才做数据从session同步到数据库，且重新更新session数据

        user_id = request.session.get('user_id')
        if user_id:
            session_goods = request.session.get('goods')
            if session_goods:
                # 1.判断session商品中是否存在数据库中，如果存在则更新，不存在则创建
                shop_carts = ShoppingCart.objects.filter(user_id=user_id)
                # 标识符flag，表示是否修改购物车中的商品信息
                data = []
                for goods in shop_carts:
                    for se_goods in session_goods:
                        if se_goods[0] == goods.goods_id:
                            goods.nums = se_goods[1]
                            goods.save()
                            # 向data中添加编辑了的商品id值
                            data.append(se_goods[0])
                # 添加
                session_goods_ids = [i[0] for i in session_goods]
                add_goods_ids = list(set(session_goods_ids) - set(data))
                for add_goods_id in add_goods_ids:
                    for session_good in session_goods:
                        if add_goods_id == session_good[0]:
                            ShoppingCart.objects.create(user_id=user_id, goods_id=add_goods_id, nums=session_good[1])
            # 同步数据库到session中
            new_shop_carts = ShoppingCart.objects.filter(user_id=user_id)
            session_new_goods = [[i.goods_id, i.nums, i.is_select] for i in new_shop_carts]
            request.session['goods'] = session_new_goods
        return response