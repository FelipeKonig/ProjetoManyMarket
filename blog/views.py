from django.shortcuts import render, get_object_or_404

def base(request):
    return render(request, 'blog/base.html')
