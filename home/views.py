from django.shortcuts import render

# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def how_to_measure(request):
    """ 
    A view to return the how to measure page 
    """
    template_name = 'home/how_to_measure.html'
    context = {}
    return render(request, 'home/how_to_measure.html')
