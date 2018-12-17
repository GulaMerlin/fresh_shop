from django.shortcuts import render

from goods.models import Goods, GoodsCategory


def index(request):
    if request.method == 'GET':
        data = {}
        # 循环商品分类
        for cate in GoodsCategory.CATEGORY_TYPE:
            # 获取当前分类下的前四个商品信息
            goods = Goods.objects.filter(category_id=cate[0])[0:4]
            # 组装成健值对,key为商品分类,value为当前分类的商品信息
            data[cate[1]] = goods

        return render(request, 'index.html', {'goods_category': data})


def detail(request, id):
    if request.method == 'GET':
        # 返回商品详细信息
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html', {'goods': goods})

def search(request):
    if request.method == 'GET':
        name =request.GET.get('search')
        goods = Goods.objects.filter(name__contains=name).first()
        if goods:
            return render(request, 'detail.html', {'goods': goods})
        else:
            data = {}
            # 循环商品分类
            for cate in GoodsCategory.CATEGORY_TYPE:
                # 获取当前分类下的前四个商品信息
                goods = Goods.objects.filter(category_id=cate[0])[0:4]
                # 组装成健值对,key为商品分类,value为当前分类的商品信息
                data[cate[1]] = goods
            return render(request, 'index.html', {'goods_category': data})

