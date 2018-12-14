from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from carts.models import ShoppingCart
from goods.models import Goods


def carts(request):
    if request.method == 'GET':
        # 返回购物车中的数据，不用区分是否登录，因为所有数据已经更新到session中
        session_goods = request.session.get('goods')
        data = []
        if session_goods:
            for se_goods in session_goods:
                goods = Goods.objects.filter(pk=se_goods[0]).first()
                nums = se_goods[1]
                price = nums * goods.shop_price
                data.append([goods, nums, price])
        # 返回给页面，需要将:[[商品对象，数量，价格]]反给页面
        return render(request, 'cart.html', {'goods_all': data})


def add_cart(request):
    if request.method == 'POST':
        # 保存到数据库中
        # 1.获取前端ajax提交的商品goods_id,商品数量nums
        # 2.组装存储到session中到数据[[goods_id, nums, is_select], [goods_id, nums, is_select]]
        # 3.如果加入到session中到商品已经存在session中，则更新num字段
        goods_id = int(request.POST.get('goods_id'))
        nums = int(request.POST.get('nums'))
        # 组装存储的结构,[商品id值, 商品数量, 商品选择状态]
        goods_list = [goods_id, nums, 1]
        # 怕断session中是否保存的购物车数据,{'goods': [[id, nums, 1], ]}
        session_goods = request.session.get('goods')
        if session_goods:
            # 添加或者修改
            flag = False
            for goods in session_goods:
                # goods为[goods_id, nums, is_select]
                if goods[0] == goods_id:
                    goods[1] += nums
                    flag = True
            # 添加
            if not flag:
                session_goods.append(goods_list)
            request.session['goods'] = session_goods
            # session中保存到商品到个数
            goods_count = len(session_goods)
        else:
            # 第一次添加到商品到session中时，保存健值对键为goods，值为[[goods_id, nums, is_select]]
            request.session['goods'] = [goods_list]
            goods_count = 1
        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'goods_count': goods_count})
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        goods_count = len(session_goods)
        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'goods_count': goods_count})


def count_cart(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        count = len(session_goods) if session_goods else 0
        return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


def change_cart(request):
    if request.method == 'POST':
        # 获取前端ajax传递的goods_id, is_select, nums
        goods_id = int(request.POST.get('goods_id'))
        is_select = request.POST.get('is_select')
        nums = request.POST.get('nums')
        # 获取session中的商品信息
        session_goods = request.session.get('goods')
        for goods in session_goods:
            # goods: [good_id, nums, is_select]
            if goods_id == goods[0]:
                goods[1] = nums if nums else goods[1]
                goods[2] = is_select if is_select else goods[2]
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def del_cart(request, id):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            ShoppingCart.objects.filter(user_id=user_id, goods_id=id).delete()

        session_goods = request.session.get('goods')
        for goods in session_goods:
            if goods[0] == int(id) :
                session_goods.remove(goods)
                break
        return HttpResponseRedirect(reverse('carts:cart'))

def is_select_cart(request):
    if request.method == 'POST':
        is_select = request.POST.get('is_select')
        goods_id = request.POST.get('goods_id')
        user_id = request.session.get('user_id')
        if user_id:
            ShoppingCart.objects.filter(user_id=user_id, goods_id=goods_id).update(is_select=is_select)
        return JsonResponse({'code': 200, 'msg': '请求成功'})




