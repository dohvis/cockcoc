from django.views.generic import (
    ListView,
)
from app.models import (
    Bar,
    Cocktail,
)


class CocktailList(ListView):
    model = Cocktail
    template_name = 'cocktail_list.html'


class BarList(ListView):
    model = Bar
    template_name = 'bar_list.html'
