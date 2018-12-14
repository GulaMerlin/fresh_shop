from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from order.models import OrderInfo
from user.forms import UserRegisterForm, UserLoginForm, UserAddressForm
from user.models import User, UserAddress
from django.contrib.auth.hashers import make_password, check_password


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['pwd']
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            if check_password(pwd, user.password):
                # 校验成功
                request.session['user_id'] = user.id
                return HttpResponseRedirect(reverse('goods:index'))
            else:
                err_pwd = '账号或密码错误'
                return render(request, 'login.html', {'err_pwd': err_pwd})
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # 字段验证成功, 用户名不存在数据库两次输入的密码一致
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['pwd']
            email = form.cleaned_data['email']
            # from django.contrib.auth.hashers import make_password
            new_password = make_password(password)
            User.objects.create(username=username, password=new_password, email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # 验证失败返回错误信息
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})


def user_center_info(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


def user_center_order(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        page = request.GET.get('page', 1)
        order_info = OrderInfo.objects.filter(user_id=user_id)
        paginator = Paginator(order_info, 5)
        page = paginator.page(page)
        return render(request, 'user_center_order.html', {'page': page})


def user_center_site(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        user_address = UserAddress.objects.filter(user_id=user_id)
        return render(request, 'user_center_site.html', {'user_address': user_address})

    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            signer_name = form.cleaned_data['signer_name']
            address = form.cleaned_data['address']
            signer_postcode = form.cleaned_data['signer_postcode']
            signer_mobile = form.cleaned_data['signer_mobile']
            user_id =request.session.get('user_id')
            UserAddress.objects.create(signer_name=signer_name, address=address, signer_postcode=signer_postcode, signer_mobile=signer_mobile, user_id=user_id)
            return HttpResponseRedirect(reverse('user:user_center_site'))
        else:
            return render(request, 'user_center_site.html', {'errors': form.errors})

