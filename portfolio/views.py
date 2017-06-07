from django.shortcuts import render
from .models import Work


def portfolio(request):
    works = Work.objects.order_by('created_date')
    return render(request, 'portfolio/portfolio.html', {'works': works})
