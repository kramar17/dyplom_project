from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from account.models import OfferModel
from djangoProject1.loger import logger
from main.forms import CallBackForm
from django.utils.translation import get_language


def main_page(request):
    """
    View function for rendering the main page.

    Retrieves visible offers and renders them along with static content.

    Returns:
        HttpResponse: Rendered HTML response.
    """
    offers = OfferModel.objects.filter(is_visible=True).order_by('sort')
    current_language = get_language()

    context = {
        'offers': offers,
        'free_consultation': _('Безкоштовна консультація'),
        'eating_plan': _('План харчування розробляється з урахуванням ваших уподобань та потреб здоров\'я'),
        'back_up_money': _('Гарантія повернення коштів протягом 5 днів'),
        'couching': _('Коучінг: спеціаліст з харчування буде слідкувати за вашим здоров\'ям'),
        'consultation_about_sport': _('Консультації по спортивному харчуванню'),
        'free_week_for_family': _('Безкоштовний тиждень для друга, чи члена вашої сім\'ї'),
        'warranty_reminder': _('*5-днівна гарантія повернення коштів включена в усі плани'),
        'current_language': current_language,

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
