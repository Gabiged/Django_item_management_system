from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
from .models import Auto, Likutis, Kategorija, Uzsakymas, UzsakymoEilute, Profilis
"""Administratoriaus puslapio atvaizdavimas"""

class KategorijaAdmin(admin.ModelAdmin):
    """pasirenkama adminsite rankiniu būdu"""
    list_display = ['name']
    list_filter = ('name', )

class LikutisResource(resources.ModelResource):
    """sukurta tam, kad galetume atsisiusti duomenis pasirinktu failo formatu (ImportExportActionModelAdmin)"""
    auto = fields.Field(column_name="eurocode", attribute="eurocode", widget=ForeignKeyWidget(Auto, 'eurocode'))

    class Meta:
        model = Likutis

class LikutisAdmin(ImportExportActionModelAdmin):
    """sukurta tam, kad galetume atsisiusti duomenis pasirinktu failo formatu (ImportExportActionModelAdmin)"""
    resource_class = LikutisResource
    list_display = ['id', 'display_auto', 'kiekis']


class AutoResource(resources.ModelResource):
    """sukurta tam, kad galetume atsisiusti duomenis pasirinktu failo formatu (ImportExportActionModelAdmin)"""
    category = fields.Field(column_name='Kategorija', attribute='Kategorija',
                            widget=ForeignKeyWidget(Kategorija, 'name'))

    class Meta:
        model = Auto


class AutoAdmin(ImportExportActionModelAdmin):
    """sukurta tam, kad galetume atsisiusti duomenis pasirinktu failo formatu (ImportExportActionModelAdmin)"""
    resource_class = AutoResource
    list_display = ('eurocode', 'pavadinimas', 'kaina', 'aprasymas', 'update')


class UzsakymoEiluteAdmin(admin.ModelAdmin):
    """čia yra užsakymo suvedimo laukai """
    list_display = ('auto_item', 'quantity', 'ketegorija')
    list_filter = ('kategorija', )


class UzsakymasInline(admin.TabularInline):
    model = UzsakymoEilute
    readonly_fields = ('id', )
    extra = 0

class UzsakymasAdmin(admin.ModelAdmin):
    """Užsakymo pagrindimiai laukai"""
    list_display = ('id',  'uzsakymo_laikas', 'pirkejas', 'suma_all', 'status', 'due_back')
    inlines = [UzsakymasInline]
    list_editable = ('status', 'due_back')
    list_filter = ('status', 'due_back',)
    search_fields = ('pirkejas',)

    fieldsets = (
        (None, {'fields': ('due_back', 'auto_tipas')
                }),
        ('Užsakymo detalės', {'fields': ('status', 'pirkejas')}),
    )


admin.site.register(Auto, AutoAdmin)
admin.site.register(Likutis, LikutisAdmin)
admin.site.register(Kategorija, KategorijaAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(Profilis)

