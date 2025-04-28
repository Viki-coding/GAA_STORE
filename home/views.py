from django.shortcuts import render

# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def how_to_measure(request):
    """ 
    A view to return the how to measure page 
    """
    return render(request, 'home/how_to_measure.html')


def faq(request):
    """ 
    A view to return the FAQ page 
    """
    return render(request, 'home/faq.html')
