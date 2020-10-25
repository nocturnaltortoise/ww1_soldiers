import json
import math

from django.shortcuts import render
from django.db.models import Q

from .models import Soldier

from django.http import JsonResponse

# Create your views here.

def index(request):
    soldier_count = Soldier.objects.order_by('surname', 'other_names').count()
    pages = int(soldier_count / 20)
    if soldier_count % 20 != 0:
        pages += 1

    soldiers = Soldier.objects.order_by('surname', 'other_names').all()[:20]
    json_soldiers = []
    for soldier in soldiers:
        json_soldiers.append({
            'surname': soldier.surname,
            'other_names': soldier.other_names,
            'rank': soldier.rank,
            'regiment': soldier.regiment,
            'soldier_number': soldier.soldier_number,
            'address': soldier.address
        })
    print(range(pages))
    return render(request, 'index.html', {'soldiers': json.dumps(json_soldiers), 'pages': list(range(10))})

def search(request):
    query = request.GET.get('q')
    page = int(request.GET['p'])
    results_per_page = 20

    soldiers = Soldier.objects
    if query:
        soldiers = soldiers.filter(
            Q(surname__icontains=query) | Q(other_names__icontains=query) | Q(regiment__icontains=query) | Q(soldier_rank__icontains=query) | Q(address__icontains=query) | Q(soldier_number__icontains=query)
        )

    soldier_count = soldiers.count()
    page_count = int(soldier_count / results_per_page)
    if soldier_count % results_per_page != 0:
        page_count += 1

    soldiers = soldiers.order_by('surname', 'other_names').all()[page*results_per_page:(page+1)*results_per_page]

    json_soldiers = {
        'soldiers': [],
        'pages': get_page_numbers(page)
    }
    for soldier in soldiers:
        json_soldiers['soldiers'].append({
            'surname': soldier.surname,
            'other_names': soldier.other_names,
            'rank': soldier.rank,
            'regiment': soldier.regiment,
            'soldier_number': soldier.soldier_number,
            'address': soldier.address
        })

    return JsonResponse(json_soldiers, safe=False)

def get_page_numbers(page):
    page = page + 1
    if page % 10 == 0:
        return list(range(page-1, page+9))

    return list(range(int(math.floor(page / 10.0)) * 10, int(math.ceil(page / 10.0)) * 10))

def about(request):
    return render(request, 'about.html')
