from django.shortcuts import render

def youts(request):
    return render(request, "youts.html", {})