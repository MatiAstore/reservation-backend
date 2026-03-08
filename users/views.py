from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hola_mundo(request):

    datos = {
        "dia": 1,
        "mes": 8
    }

    return render(request,"base.html", datos)

