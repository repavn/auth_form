from django.views.generic.edit import FormView

from custom_auth.forms import UserForm


class UserView(FormView):
    template_name = 'base.html'
    form_class = UserForm
    success_url = '/success/'

    def form_valid(self, form):
        return super().form_valid(form)
