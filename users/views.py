from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "rladlsgh654@naver.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
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
        return render(request, "users/login.html", {"form": form})

def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
# Create your views here.
