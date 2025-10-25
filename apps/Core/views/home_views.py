from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    """Vista principal del dashboard"""
    context = {
        'user': request.user,
    }
    return render(request, 'core/home.html', context)
