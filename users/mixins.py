from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

# ~mixins : url로 접근을 못하게 하는 class

class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    # test func라 false를 리턴하면 아래 핸들러를 실행
    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there"))
        return redirect(reverse("core:home"))

class LoggedOutOnlyView(UserPassesTestMixin):

    def test_func(self):
        return not self.request.user.is_authenticated

    # test func라 false를 리턴하면 아래 핸들러를 실행
    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there!"))
        return redirect(reverse("core:home"))

class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
