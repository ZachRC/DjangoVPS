from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()

class SuperUserLoginView(LoginView):
    template_name = 'superuserapp/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Log in the user and ensure they are superusers."""
        user = form.get_user()
        if not user.is_superuser:
            form.add_error(None, "You do not have permission to access this page.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('superuserapp:panel')

class PanelView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'superuserapp/panel.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template_name, {'users': users})
