from django.shortcuts import render


def purview_index(request):
    return render(request, 'homepage.html')

def purview_blog(request):
    return render(request, 'blog.html')