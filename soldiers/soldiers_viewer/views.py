import json

from django.shortcuts import render
from django.db.models import Q

from .models import Soldier

from django.http import JsonResponse

# Create your views here.

def index(request):
    soldiers = Soldier.objects.order_by('surname', 'other_names').all()
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
    return render(request, 'index.html', {'soldiers': json.dumps(json_soldiers)})

def search(request):
    query = request.GET.get('q')

    soldiers = Soldier.objects
    if query:
        soldiers = soldiers.filter(
            Q(surname__icontains=query) | Q(other_names__icontains=query) | Q(regiment__icontains=query) | Q(soldier_rank__icontains=query) | Q(address__icontains=query) | Q(soldier_number__icontains=query)
        )

    soldiers = soldiers.order_by('surname', 'other_names').all()

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

    return JsonResponse(json_soldiers, safe=False)

def about(request):
    return render(request, 'about.html')
