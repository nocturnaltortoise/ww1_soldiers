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

    def friendly_version(self, conversion_dict, original):
        words = re.findall(r"[\w']+", original)

        friendly_version = ""
        for word in words:
            friendly_version += " " + (conversion_dict.get(word) or word)

        return friendly_version.strip()

    @property
    def friendly_rank(self):
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

        return self.friendly_version(ranks, self.soldier_rank)

    @property
    def friendly_regiment(self):
        regiment_codes = {
            "Fus": "Fusiliers",
            "Rgt": "Regiment",
            "Coy": "Company",
            "Cpy": "Company",
            "Bde": "Brigade",
            "RFA": "Royal Field Artillery",
            "RGA": "Royal Garrison Artillery",
            "KOR": "King's Own Rifles",
            "Lancs": "Lancashire"
        }

        return self.friendly_version(regiment_codes, self.regiment)
