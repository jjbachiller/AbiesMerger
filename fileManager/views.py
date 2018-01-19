from django.shortcuts import redirect, render
from abiesmerger.engine.abiesmanager import AbiesManager

def home_page(request):
    return render(request, 'home.html')

def merge(request):
    errors = []
    bbase = request.FILES['input-bbase']
    if (not bbase):
        errors.append('Debe indicar la biblioteca base')
    bsecundariaList = request.FILES.getlist('input-bsecundaria[]')
    if (not all(bsecundariaList)):
        errors.append('Debe añadir al menos una biblioteca secundaria')

    if (not errors):
        try:
            manager = AbiesManager(bbase, bsecundariaList, [])
            manager.merge()
            return redirect('download')
        except Exception as error:
            errors.append(repr(error))

    return render(request, 'home.html', {'errors': errors})


def download(request):
    return render(request, 'download.html')
