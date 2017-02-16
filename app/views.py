from django.views.generic import (
    DetailView,
    ListView,
)
from app.models import (
    Bar,
    Cocktail,
)


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
