from django.shortcuts import render, redirect
from account.models import OfferModel
from main.forms import CallBackForm
from django.contrib import messages


def main_page(request):
    offers = OfferModel.objects.all().filter(is_visible=True).order_by('sort')
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
    if request.method == 'POST':
        form = CallBackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка на дзвінок прийнята!')
            return redirect('/')
    else:
        form = CallBackForm()
    return render(request, 'callback.html', {'form': form})

