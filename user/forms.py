from django import forms

from user.models import User


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(min_length=5, max_length=20, required=True, error_messages={
                                'required': '用户名必填',
                                'min_length': '用户名不能少于5个字符',
                                'max_length': '用户名不能超过20个字符'
                                })
    pwd = forms.CharField(required=True, min_length=8, max_length=20, error_messages={
                                'required': '密码必填',
                                'min_length': '密码不能少于8个字符',
                                'max_length': '密码不能超过20个字符'
                                })
    cpwd = forms.CharField(required=True, min_length=8, max_length=20, error_messages={
                                'required': '密码必填',
                                'min_length': '密码不能少于8个字符',
                                'max_length': '密码不能超过20个字符'
                                })
    email = forms.CharField(required=True, error_messages={
                            'required': '邮箱必填'
                                })
    # 验证时会自动调用
    def clean(self):
        # 校验用户名是否已存在于数据库
        user = User.objects.filter(username=self.cleaned_data.get('user_name')).first()
        if user:
            # 验证用户已存在数据库,抛出异常
            raise forms.ValidationError({'user_name': '该用户已注册！'})
        # 校验密码是否相等
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'pwd': '两次密码不一致！'})

        return self.cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=20, required=True, error_messages={
                                'required': '用户名必填',
                                'min_length': '用户名不能少于5个字符',
                                'max_length': '用户名不能超过20个字符'
                                })
    pwd = forms.CharField(required=True, min_length=8, max_length=20, error_messages={
                                'required': '密码必填',
                                'min_length': '密码不能少于8个字符',
                                'max_length': '密码不能超过20个字符'
                                })
    def clean(self):
        # 验证登录的账号是否已经注册
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        if not user:
            raise forms.ValidationError({'username': '该账号未注册'})
        return self.cleaned_data

class UserAddressForm(forms.Form):
    signer_name = forms.CharField(required=True, error_messages={
                                'required': '收件人必填'
    })
    address = forms.CharField(required=True, error_messages={
                                'required': '详细地址必填'
    })
    signer_postcode = forms.CharField(required=True, error_messages={
                                'required': '邮箱必填'
    })
    signer_mobile = forms.CharField(required=True,max_length=11, min_length=11, error_messages={
                                'required': '电话必填',
                                'max_value': '电话最长11个字符',
                                'min_value': '电话最短11个字符'
    })
