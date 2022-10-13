import django_tables2 as tables
from .models import Auto
"""Lentele, kurioje pateikiamas visų prekių sąrašas, taip pat ir prisijungimo nuspalvinti laukai"""
class AutoTable(tables.Table):
    class Meta:
        model = Auto
        template_name = "django_tables2/bootstrap.html"
        fields = ("eurocode", "pavadinimas", )