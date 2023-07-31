from django import forms
from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth import forms as auth_forms
from django.urls import reverse_lazy
from django.views import generic as view

UserModel = get_user_model()
print(UserModel)

class RegisterUserForm(auth_forms.UserCreationForm):
    consent = forms.BooleanField()

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email', )




class RegisterUserView(view.CreateView):
    template_name = 'app_auth/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main_view')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result


class LoginUserView(auth_views.LoginView):
    template_name = 'app_auth/login.html'


class LogoutUserView(auth_views.LogoutView):
    pass