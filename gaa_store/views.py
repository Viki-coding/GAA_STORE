from django.shortcuts import render


def handle_404(request, exception):
    """
    Custom 404 error handler.
    """
    return render(request, 'errors/404.html', status=404)


def handle_500(request):
    """
    Custom 500 error handler.
    """
    return render(request, 'errors/500.html', status=500)

    