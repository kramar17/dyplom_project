from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth import logout, authenticate, login
from account.forms import LoginForm, RegisterForm
from account.models import OfferModel, UserDiscount, DietitianClient


class RegisterView(CreateView):
    """
    View for user registration.

    Attributes:
        template_name (str): Template file path for rendering the registration form.
        form_class (class): Form class used for user registration.
        success_url (str): URL to redirect after successful registration.
    """

    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        Process the valid form submission.

        Args:
            form (Form): Validated form instance.

        Returns:
            HttpResponse: Redirects to success URL after saving the form.
        """
        form.save()
        return super().form_valid(form)


class MyLoginView(FormView):
    """
    View for user login.

    Attributes:
        template_name (str): Template file path for rendering the login form.
        form_class (class): Form class used for user login.
        success_url (str): URL to redirect after successful login.
    """

    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        """
        Process the valid form submission.

        Args:
            form (Form): Validated form instance.

        Returns:
            HttpResponse: Redirects to success URL after authentication.
        """
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
    """
    View for user logout.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirects to the home page after logout.
    """
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    """
    View for user profile.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders the user profile page with necessary context data.
    """
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

    recommendation = "Поки нема рекомендацій"
    try:
        dietitian_client = DietitianClient.objects.get(client=user)
        recommendation = dietitian_client.recommendation
    except DietitianClient.DoesNotExist:
        pass

    context = {
        'user': user,
        'offers': offers,
        'monthly_payment': monthly_payment,
        'recommendation': recommendation
    }
    return render(request, 'profile.html', context)


@staff_member_required
def manager_profile_view(request):
    """
    View for manager profile.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders the manager profile page with necessary context data.
    """
    clients = DietitianClient.objects.filter(dietitian=request.user).select_related('client')
    manager_first_name = request.user.first_name
    manager_last_name = request.user.last_name

    context = {
        "manager_first_name": manager_first_name,
        "manager_last_name": manager_last_name,
        'clients': clients
    }
    return render(request, 'manager_profile.html', context)


def client_profile_view(request, client_id):
    """
    View for client profile.

    Args:
        request (HttpRequest): The request object.
        client_id (int): ID of the client.

    Returns:
        HttpResponse: Renders the client profile page with necessary context data.
    """
    client = get_object_or_404(DietitianClient, pk=client_id)
    if request.method == 'POST':
        recommendation = request.POST.get('recommendation')
        client.recommendation = recommendation
        client.save()
        return redirect('client_profile', client_id=client_id)

    return render(request, 'client_profile.html', {'client': client})
