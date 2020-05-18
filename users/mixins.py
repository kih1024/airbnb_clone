from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

# ~mixins : url로 접근을 못하게 하는 class

class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    # test func라 false를 리턴하면 아래 핸들러를 실행
    def handle_no_permission(self):
        messages.error(self.request, "다른 회원으로는 접근할 수 없습니다.")
        return redirect(reverse("core:home"))

class LoggedOutOnlyView(UserPassesTestMixin):

    def test_func(self):
        return not self.request.user.is_authenticated

    # test func라 false를 리턴하면 아래 핸들러를 실행
    def handle_no_permission(self):
        messages.error(self.request, "로그인 상태로 접속할 수 없습니다!")
        return redirect(reverse("core:home"))

class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
