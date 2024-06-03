from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth import logout, authenticate, login
from account.forms import LoginForm
from account.forms import RegisterForm
from account.models import OfferModel, UserDiscount


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class MyLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Невірний логін чи пароль')
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    user = request.user
    offers = OfferModel.objects.all()
    monthly_payment = None

    user_discounts = UserDiscount.objects.filter(user=user)
    if user_discounts.exists():
        for offer in offers:
            user_discount = user_discounts.first()
            offer.discounted_price = offer.price * (1 - user_discount.discount.percentage / 100)
        monthly_payment = sum(offer.discounted_price for offer in offers)
    else:
        monthly_payment = None

    return render(request, 'profile.html', {'user': user, 'offers': offers, 'monthly_payment': monthly_payment})
