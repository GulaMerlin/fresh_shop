from django.http import JsonResponse
from django.shortcuts import render

from carts.models import ShoppingCart
from order.models import OrderInfo, OrderGoods
from user.models import UserAddress


def place_order(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        shop_carts = ShoppingCart.objects.filter(user_id=user_id, is_select=1)
        # 给购物车中的对象绑定一个新增的属性，其值的为小记
        all_total = 0
        for carts in shop_carts:
            price = carts.nums * carts.goods.shop_price
            carts.total = price
            all_total += price
        carts_count = len(shop_carts)
        return render(request, 'place_order.html',
                      {'shop_carts': shop_carts,
                       'all_total':all_total,
                       'carts_count': carts_count})


def make_order(request):
    if request.method == 'POST':
        # 创建订单
        # 创建订单详情
        # 购物车中删除已经下单的商品
        user_id = request.session['user_id']
        # 去购物车中勾选的商品
        shop_carts = ShoppingCart.objects.filter(user_id=user_id, is_select=1)

        # 计算总价
        order_mount = 0
        for carts in shop_carts:
            order_mount += carts.nums * carts.goods.shop_price
        # 生成订单交易号
        from utils.functions import get_order_sn
        order_sn = get_order_sn()

        address_id = request.POST.get('address_id')
        user_address = UserAddress.objects.filter(pk=address_id).first()
        order = OrderInfo.objects.create(user_id=user_id,
                                         order_sn=order_sn,
                                         order_mount=order_mount,
                                         address=user_address,
                                         signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile)

        # 创建订单详情
        for carts in shop_carts:
            OrderGoods.objects.create(order=order,
                                      goods=carts.goods,
                                      goods_nums=carts.nums, )
        # 删除购物车中的商品
        shop_carts.delete()
        request.session.pop('goods')

        return JsonResponse({'code': 200, 'msg': '创建成功'})