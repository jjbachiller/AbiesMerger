from django.shortcuts import redirect, render
from abiesmerger.engine.abiesfile import AbiesFile

def home_page(request):
    return render(request, 'home.html')

def merge(request):
    errors = []
    if (not request.POST['input-bbase']):
        errors.append('Debe indicar la biblioteca base')
    bsecundariaList = request.POST.getlist('input-bsecundaria[]')
    if (not all(bsecundariaList)):
        errors.append('Debe añadir al menos una biblioteca secundaria')

    if (not errors):
        aFile = AbiesFile(request.POST['input-bbase'])
        return redirect('download')
    else:
        return render(request, 'home.html', {'errors': errors})


def download(request):
    return render(request, 'merge.html')
