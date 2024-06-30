from django.shortcuts import render, redirect
from django.contrib import messages
from account.models import OfferModel
from djangoProject1.loger import logger
from main.forms import CallBackForm


def main_page(request):
    """
    View function for rendering the main page.

    Retrieves visible offers and renders them along with static content.

    Returns:
        HttpResponse: Rendered HTML response.
    """
    offers = OfferModel.objects.filter(is_visible=True).order_by('sort')
    free_consultation = 'Безкоштовна консультація'
    eating_plan = 'План харчування розрозблюється з урахуванням ваших уподобань та потреб здоровья'
    back_up_money = 'Гарантія повернення коштів протягом 5 днів'
    couching = 'Коучінг: спеціаліст з харчування буде слідкувати за вашим здоров`ям'
    consultation_about_sport = 'Консультації по спортивному харчуванню'
    free_week_for_family = 'Безкоштовний тиждень для друга, чи члена вашої сім`ї'
    warranty_reminder = '*5-днівна гарантія повернення коштів включена в усі плани'

    context = {
        'offers': offers,
        'free_consultation': free_consultation,
        'eating_plan': eating_plan,
        'back_up_money': back_up_money,
        'couching': couching,
        'consultation_about_sport': consultation_about_sport,
        'free_week_for_family': free_week_for_family,
        'warranty_reminder': warranty_reminder,
    }

    return render(request, 'index.html', context)


def callback_view(request):
    """
    View function for handling callback form submissions.

    Accepts POST requests with form data, validates and saves the form,
    then redirects to the main page with a success message. If the request
    method is GET, renders an empty callback form.

    Returns:
        HttpResponse: Rendered HTML response.
    """
    if request.method == 'POST':
        form = CallBackForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(
                f"Заявка на зворотний дзвінок від {form.cleaned_data.get('name')},"
                f" телефон: {form.cleaned_data.get('phone')}")
            messages.success(request, 'Заявка на дзвінок прийнята!')
            return redirect('/')
    else:
        form = CallBackForm()

    return render(request, 'callback.html', {'form': form})
