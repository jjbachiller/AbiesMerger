from django.shortcuts import redirect, render

def home_page(request):
    return render(request, 'home.html')

def upload(request):
    error = None
    print(request.POST.getlist('input-bsecundaria[]'))
    if (len(request.POST.getlist('input-bsecundaria[]')) > 1):
        print("Longitud: " + str(len(request.POST.getlist('input-bsecundaria'))))
        print(request.POST.getlist('input-bsecundaria'))
        error = 'No se puede añadir más que una biblioteca secundaria'

    if (error is None):
        return redirect('merge')
    else:
        return render(request, 'home.html', {'error': error})


def merge(request):
    return render(request, 'merge.html')
