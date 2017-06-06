from django.shortcuts import render


def portfolio_list(request):
    return render(request, 'portfolio/portfolio_list.html', {})
