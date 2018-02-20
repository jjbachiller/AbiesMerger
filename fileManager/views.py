import os
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from abiesmerger.engine.abiesmanager import AbiesManager
from django.conf import settings
from django.utils.encoding import smart_str
from django.contrib import messages

def home_page(request):
    return render(request, 'home.html')

def merge(request):
    # TODO: Ver como validar con un form.
    bbase = request.FILES.get('input-bbase', False)
    if (not bbase):
        messages.add_message(request, messages.ERROR, 'Debe indicar la biblioteca base.')
    bsecundariaList = request.FILES.getlist('input-bsecundaria[]')
    if (not bsecundariaList):
        messages.add_message(request, messages.ERROR, 'Debe añadir al menos una biblioteca secundaria.')
    suffixes = request.POST.getlist('suffixes[]')

    if (not messages.get_messages(request)):
        try:
            manager = AbiesManager(bbase, bsecundariaList, suffixes)
            downloadId = manager.merge()
            return redirect(reverse('download', kwargs={'folder':downloadId,}))
        except Exception as error:
            messages.add_message(request, messages.ERROR, repr(error))
            raise(error)
    return redirect('home')


def download(request, folder):
    path = os.path.join(settings.DOWNLOAD_FOLDER, folder, settings.ABIES_ZIP_FILE)
    if (not os.path.isfile(path)):
        messages.add_message(request, messages.ERROR, 'No existe el archivo para descargar.')
        return redirect('home')
    return render(request, 'download.html', {'path': path})
