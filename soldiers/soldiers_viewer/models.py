import re
from django.db import models

# Create your models here.

class Soldier(models.Model):
    other_names = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    regiment = models.CharField(max_length=50, null=True)
    soldier_rank = models.CharField(max_length=20, null=True)
    soldier_number = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)

    @property
    def rank(self):
        ranks = {
            'Cpl': 'Corporal',
            'L': 'Lance',
            'Pte': 'Private',
            'A': 'Acting',
            'Gnr': 'Gunner',
            'Dvr': 'Driver',
            'Sgt': 'Sergeant',
            'Lieut': 'Lieutenant',
            '2': '2nd',
            '1': '1st',
            'Capt': 'Captain',
            'Cpt': 'Captain'
        }
        rank_parts = re.findall(r"[\w']+", self.soldier_rank)

        friendly_rank = ""
        for part in rank_parts:
            friendly_rank += " " + (ranks.get(part) or part)

        return friendly_rank.strip()
