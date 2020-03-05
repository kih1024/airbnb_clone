from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            # check_password는 password를 암호화해서 디비에 암호화된 비번과 비교한다.
            if user.check_password(password):
                return self.cleaned_data
            else:
                # raise forms.ValidationError("Password is wrong")  #이렇게 하면 어디 field에서 에러가 왔는지 모름. 실제로 nonefield라 나왔있음. 그래서 아래처럼 하면
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            # raise forms.ValidationError("User does not exist")
            self.add_error("email", forms.ValidationError("User does not exist"))

    # 이건 내가 만든 이름이 아니다 . 무엇인가를 이메일이나 비밀번호가 있는 field를 확인 하고 싶으면 method 이름을 clean_ 으로 해야함.
    # def clean_email(self):
    #     # print(self.cleaned_data)
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")
