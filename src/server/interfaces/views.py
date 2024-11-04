from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DataBaseInstace, AgentToken
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
import random
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
import uuid

def create_random_pwd(length):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    password = ''
    for _ in range(length):
        password += chars[random.randint(0,len(chars)-1)]
    return password


def get_db_avail_port():
    while True:
        port = random.randint(20_000,30_000)
        dbs = DataBaseInstace.objects.filter(port=port)
        if not dbs:
            break
    return port

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
            dbi.instance_cpu = 0.1
            dbi.instance_ram = 128
            dbi.instance_disk = 100
            dbi.password = create_random_pwd(128)
            dbi.port = get_db_avail_port()
            dbi.status = 'on-creation'
            dbi.save()

            return render(request, 'interfaces/database_create_show_pwd.html', context={'responses':responses, 'dbi':dbi})

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
            dbi.status = 'on-deletion'
            dbi.save()
            return HttpResponseRedirect('/databases/')

    return render(request, 'interfaces/database_delete.html', context={'responses':responses,'dbi':dbi})

def agent_communication(request, id):
    # Check if token exists and is valid

    tokens = AgentToken.objects.all()
    check = False
    for token in tokens:
        if id in str(token.uuid):
            check=True
    if check == False:
        return HttpResponse('Unauthorized', status=401)
        
    if request.method == 'GET':
        dbis = DataBaseInstace.objects.exclude(status='done')
        
        data = {}
        for dbi in dbis:
            data[f'{dbi.owner.id}-{dbi.id}'] = {
                'status': dbi.status,
                'userid': dbi.owner.id,
                'dbiid': dbi.id,
                'cpu': dbi.instance_cpu,
                'ram': dbi.instance_ram,
                'disk': dbi.instance_disk,
                'password': dbi.password,
                'port': dbi.port,
            }

        return JsonResponse(data, status=200)
    
    elif request.method == 'POST':
        # Add POST handling logic here if needed
        return JsonResponse({'message': 'POST request handled'}, status=200)
    
    else:
        return HttpResponse('Method not allowed', status=405)
