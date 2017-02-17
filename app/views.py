from django.views.generic import (
    DetailView,
    ListView,
)
from .serializers import BarSerializer
from rest_framework import viewsets
from rest_framework.response import Response
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

    def get_context_data(self, **kwargs):
        context = super(BarDetail, self).get_context_data(**kwargs)
        context['cocktails'] = Cocktail.objects.all()[:5]
        return context

def login(request):
    return render(request, template_name='login.html')


def register(request):
    return render(request, template_name='register.html')


def select_tags(request):
    return render(request, template_name='select_tags.html')


def index(request):
    cocktails = Cocktail.objects.all()
    context = {'cocktails': cocktails}
    return render(request, template_name='index.html', context=context)


class BarViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BarSerializer
    read_only = True
    queryset = Bar.objects.all()

    def list(self, request, *args, **kwargs):
        ne = [float(x) for x in self.request.query_params.get('ne', '43.0,132.0').split(",")]
        sw = [float(x) for x in self.request.query_params.get('sw', '33.0,124.0').split(",")]
        # 우리나라 위도 경도 범위 참고해서 우리나라 전범위
        # 위도(y),경도(x) 범위: (124.0, 132.0) (33.0, 43.0)
        lat_range = (sw[1], ne[1],)
        lng_range = (sw[0], ne[0],)
        print(lat_range, lng_range)
        queryset = Bar.objects.filter(lat__range=lat_range, lng__range=lng_range)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
