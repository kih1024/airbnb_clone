import os
import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    # 그냥 reverse를 사용하면 view을 불러올때 url이 아직 불려지지 않아서 오류가 발생한다.(lazy : 실행하지 않는다) 그래서 view가 필요할떄만 호출하는 reverse_lazy라는 것을 사용한다고 한다.
    success_url = reverse_lazy("core:home")
    initial = {"email": "rladlsgh654@naver.com"}

    # 이 함수는 그전에 구현했던 ( form = forms.LoginForm(request.POST) ; if form.is_valid(): ) 부분을 대체해준다. 말 그대로 폼이 유효한지 체크
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
        # 이게 호출시 success_url로 가고 작동한다. render 할 필요가 없음.


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))

    """ def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # 클린데이터는 form에서 입력받은 데이터다.
            # forms에서 clean_메소드가 아무것도 리턴안하면 그 필드들을 지워 버린다. 만약 그 clean 메소드가 없으면 그대로 클린 데이터를 가져옴
            # 따라서 clean 메소드에서 클린 데이터를 리턴하면 클린 데이터를 가져올수 있음.
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
            # print(form.cleaned_data)
        return render(request, "users/login.html", {"form": form}) """


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "inho",
        "last_name": "kim",
        "email": "rladlsgh654@naver.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


# aceess 토큰을 위한 code를 받기 위한 함수
def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            # code로 부터 받은 access 토큰을 추출했다
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                print(profile_json)
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        # 암호를 통한 로그인 x, 외부인증 OAuth에 의한 유저 이기 때문. 이 설정은 save를 하지 않음. 따라서 따로 save 해야함.
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse("users:login"))


#                      if user is not None:
#                         return redirect(reverse("users:login"))
#                     else:
#                         user = models.User.objects.create(
#                             username=email, first_name=name, bio=bio, email=email
#                         )
#                         login(request, user)
#                         return redirect(reverse("core:home"))
# # Create your views here.
# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "rladlsgh654@naver.com"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             # 클린데이터는 form에서 입력받은 데이터다.
#             # forms에서 clean_메소드가 아무것도 리턴안하면 그 필드들을 지워 버린다. 만약 그 clean 메소드가 없으면 그대로 클린 데이터를 가져옴
#             # 따라서 clean 메소드에서 클린 데이터를 리턴하면 클린 데이터를 가져올수 있음.
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#             # print(form.cleaned_data)
#         return render(request, "users/login.html", {"form": form})

# def log_out(request):
#     logout(request)
#     return redirect(reverse("core:home"))
# # Create your views here.
