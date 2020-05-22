from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from custom_auth.costants import ACTION_REGISTER, ACTION_LOGIN
from custom_auth.forms import UserForm


class UserView(FormView):
    template_name = 'base.html'
    form_class = UserForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['ACTION_REGISTER'] = ACTION_REGISTER
        context['ACTION_LOGIN'] = ACTION_LOGIN
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        username = cleaned_data['username']
        password = cleaned_data['password']
        action_type = cleaned_data.get('action_type', '').strip()
        if action_type == ACTION_LOGIN:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(self.request, user)
        return super(UserView, self).form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/')
