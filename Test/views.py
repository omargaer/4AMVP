from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from Test.models import CompanyGroup, Application, IndividualEntity, Device
from Test.queries.company_queries import get_all_groups


# Create your views here.
def auth(request):
    if request.method == 'GET':
        return render(request, 'Test/auth.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'Test/main.html')
        else:
            return render(request, 'Test/auth.html', {'error': 'Неверные данные'})
    return None

def load_menu(request):
    menu_type = request.GET.get('type')
    context = {}
    if menu_type == 'companies':
        companies = get_all_groups()
        context['companies'] = companies
        template = 'Test/companies.html'
    elif menu_type == 'apps':
        applications = Application.objects.all()
        context['applications'] = applications
        template = 'Test/apps.html'

    elif menu_type == 'users':
        users = IndividualEntity.objects.all()
        context['users'] = users
        template = 'Test/users.html'

    elif menu_type == 'wares':
        devices = Device.objects.all()
        context['devices'] = devices
        template = 'Test/wares.html'
    else:
        return HttpResponseBadRequest('Неверный тип меню')

    return render(request, template, context)