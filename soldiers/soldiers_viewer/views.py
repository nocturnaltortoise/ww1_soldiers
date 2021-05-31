import json
import math

from django.shortcuts import render
from django.db.models import Q

from .models import Soldier

from django.http import JsonResponse

# Create your views here.

def index(request):
    soldier_count = Soldier.objects.order_by('surname', 'other_names').count()
    pages = int(soldier_count / 10)
    if soldier_count % 10 != 0:
        pages += 1

    soldiers = Soldier.objects.order_by('surname', 'other_names').all()[:10]
    json_soldiers = []
    for soldier in soldiers:
        json_soldiers.append({
            'surname': soldier.surname,
            'other_names': soldier.other_names,
            'rank': soldier.friendly_rank,
            'original_rank': soldier.soldier_rank,
            'regiment': soldier.friendly_regiment,
            'original_regiment': soldier.regiment,
            'soldier_number': soldier.soldier_number,
            'address': soldier.address,
            'lat': float(soldier.lat) if soldier.lat else '',
            'lng': float(soldier.lng) if soldier.lng else '',
            'id': soldier.id
        })

    return render(request, 'index.html', {'soldiers': json.dumps(json_soldiers), 'pages': list(range(10))})

def search(request):
    query = request.GET.get('q')
    page = int(request.GET['p'])
    results_per_page = 10

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
            'rank': soldier.friendly_rank,
            'original_rank': soldier.soldier_rank,
            'regiment': soldier.friendly_regiment,
            'original_regiment': soldier.regiment,
            'soldier_number': soldier.soldier_number,
            'address': soldier.address,
            'lat': float(soldier.lat) if soldier.lat else '',
            'lng': float(soldier.lng) if soldier.lng else '',
            'id': soldier.id
        })

    return JsonResponse(json_soldiers, safe=False)


def map(request):
    return render(request, 'map.html')

def map_data(request):
    soldiers = Soldier.objects.exclude(lat__isnull=True)
    map_markers = []

    for soldier in soldiers:
        map_markers.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(soldier.lng), float(soldier.lat)]
            }
        })

    return JsonResponse({'type': 'FeatureCollection', 'features': map_markers}, safe=False)


def get_page_numbers(page):
    page = page + 1
    if page % 10 == 0:
        return list(range(page-1, page+10))

    start_of_ten_pages = max((int(math.floor(page / 10.0)) * 10)-1, 0)
    return list(range(start_of_ten_pages, int(math.ceil(page / 10.0)) * 10))

def about(request):
    return render(request, 'about.html')
