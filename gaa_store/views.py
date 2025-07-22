from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string


def sitemap_view(request):
    xml_content = render_to_string("sitemap.xml")  # or generate dynamically
    return HttpResponse(xml_content, content_type="application/xml")


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /profile/\n"
        "Disallow: /checkout/\n"
        "\n"
        "Sitemap: https://gaastore-2f38a7e53edc.herokuapp.com/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")


def handle_404(request, exception):
    """
    Custom 404 error handler.
    """
    return render(request, '404.html', status=404)


def handle_500(request):
    """
    Custom 500 error handler.
    """
    return render(request, '500.html', status=500)
