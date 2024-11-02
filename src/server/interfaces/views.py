from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DataBaseInstace
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect


# Create your views here.
def home(request):
    return render(request, 'interfaces/home.html')

@login_required(login_url='/auth_app/login/')
def databases(request):

    databases = DataBaseInstace.objects.filter(owner=User.objects.get(id=request.user.id))

    return render(request, 'interfaces/databases.html', context={'databases':databases})

@login_required(login_url='/auth_app/login/')
def database_create(request):
    responses = []

    if request.method == 'POST':

        if DataBaseInstace.objects.filter(owner=User.objects.get(id=request.user.id), name=request.POST['databasename']):
            responses.append('You already have a database with this name.')

        if not responses:
            dbi = DataBaseInstace()
            dbi.name = request.POST['databasename']
            dbi.owner = User.objects.get(id=request.user.id)
            dbi.save()
            return HttpResponseRedirect('/databases/')

    return render(request, 'interfaces/database_create.html', context={'responses':responses})

@login_required(login_url='/auth_app/login/')
def database_management(request,id):
    responses = []

    if not DataBaseInstace.objects.filter(owner=User.objects.get(id=request.user.id), id=id):
        responses.append('NOT ALLOWED TO SEE THIS CONTENT.')

    if not responses:
        dbi = DataBaseInstace.objects.get(id=id)

    return render(request, 'interfaces/database_management.html', context={'responses':responses,'dbi':dbi})


@login_required(login_url='/auth_app/login/')
def database_delete(request,id):
    responses = []

    if not DataBaseInstace.objects.filter(owner=User.objects.get(id=request.user.id), id=id):
        responses.append('NOT ALLOWED TO SEE THIS CONTENT.')

    if not responses:
        dbi = DataBaseInstace.objects.get(id=id)

        if request.method == 'POST':
            dbi.delete()
            return HttpResponseRedirect('/databases/')

    return render(request, 'interfaces/database_delete.html', context={'responses':responses,'dbi':dbi})