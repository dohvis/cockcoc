from django.views.generic import (
    DetailView,
    ListView,
)
from app.models import (
    Bar,
    Cocktail,
)
from django.shortcuts import render


class CocktailList(ListView):
    model = Cocktail
    template_name = 'cocktail_list.html'


class CocktailDetail(DetailView):
    model = Cocktail
    template_name = 'cocktail_detail.html'


class BarList(ListView):
    model = Bar
    template_name = 'bar_list.html'


class BarDetail(DetailView):
    model = Bar
    template_name = 'bar_detail.html'


def login(request):
    return render(request, template_name='login.html')


def register(request):
    return render(request, template_name='register.html')


def select_tags(request):
    return render(request, template_name='select_tags.html')
