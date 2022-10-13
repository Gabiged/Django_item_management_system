from django.db import models
import sys
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from PIL import Image


class Kategorija(models.Model):
    """modelis, kuris nurodo automobilio tipą, pasirenkamas tik duomenų įvedimo metu"""
    name = models.CharField("Kategorija", max_length=20)

    class Meta:
        """nurodome, kaip turi būti atvaizduojami laukai Admin puslapyje"""
        verbose_name_plural = "Kategorijos"

    def __str__(self):
        return f"{self.name}"


class Likutis(models.Model):
    """Sandėlio likučiai"""
    kiekis = models.IntegerField('Likutis', default=0)

    class Meta:
        verbose_name_plural = "Likučiai"

    def get_absolute_url(self):
        return reverse('likutis-detail', args=[str(self.id)])

    def display_auto(self):
        return ', '.join(auto.eurocode for auto in self.auto_link.all()[:3])

    display_auto.short_description = "Eurokodas"

    def __str__(self):
        return f"{self.kiekis}"


class Auto(models.Model):
    """klasėje visa informacija apie prekę"""
    eurocode = models.CharField('Eurocode', max_length=30)
    pavadinimas = models.CharField('Modelis', max_length=50)
    kategorija = models.ForeignKey("Kategorija", on_delete=models.SET_NULL, null=True, related_name='kategorijos')
    kaina = models.DecimalField("Kaina, Eur", max_digits=5, decimal_places=2)
    aprasymas = models.TextField('Sudėtis', max_length=300)
    update = models.DateField('Atnaujinta', auto_now_add=True)
    lik = models.ForeignKey('Likutis', on_delete=models.SET_NULL, null=True, related_name='auto_link')

    class Meta:
        verbose_name_plural = "Automobilis"

    def get_absolute_url(self):
        return reverse('auto-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self. eurocode}, {self.pavadinimas}'

class Uzsakymas(models.Model):
    """klasė prekės užsakymas, kuriame priskiriamas pirkėjas ir nustatomi datų laukai, užsakymo statusas"""
    auto_tipas = models.ForeignKey('Kategorija', on_delete=models.SET_NULL, null=True, related_name='category')
    auto = models.ForeignKey('Auto', on_delete=models.SET_NULL, null=True, related_name='autos')
    pirkejas = models.ForeignKey(User, models.CASCADE, null=True)
    uzsakymo_laikas = models.DateField(auto_now_add=True)
    due_back = models.DateField("Užsakymo įvykdymo data", null=True, blank=True)

    UZSAKYMAS_STATUS = (
        ('a', 'Apdorojama'),
        ('g', "Galima paimti"),
        ('l', 'Įvykdyta'),
    )

    status = models.CharField(max_length=1, choices=UZSAKYMAS_STATUS, blank=True, default="a", help_text='statusas')

    class Meta:
        verbose_name_plural = "Užsakymas"
        ordering = ["due_back"]

    @property
    def is_overdue(self):
        """skaičiuoja ar nevėluojama su užsakymo pristatymu, atsispindi užsakymo detaliam vaizde"""
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def suma_all(self):
        """sumuojama užsakymo vertė, price atkeliauja iš užsakymoEilutės"""
        kainos = [e.price_sum for e in UzsakymoEilute.objects.filter(uzsakymas_item=self.id).all()]
        suma = sum(kainos)
        return f'{suma} Eur'

    suma_all.short_description = "suma"

    def get_absolute_url(self):
        return reverse('uzsakymas-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.id}. užsakymo data: {self.uzsakymo_laikas}, {self.auto}, užsakovas: {self.pirkejas.username}," \
               f"{self.due_back}, {self.status}"


class UzsakymoEilute(models.Model):
    """detalizuojamas užsakymas"""
    auto_item = models.ForeignKey('Auto', on_delete=models.SET_NULL, null=True, related_name='auto_items')
    uzsakymas_item = models.ForeignKey("Uzsakymas", on_delete=models.SET_NULL, null=True, related_name='orders')
    quantity = models.PositiveIntegerField('Prekės kiekis', null=False, help_text='Iveskite prekės kiekį')

    class Meta:
        verbose_name_plural = "Užsakymo eilutė"

    @property
    def price_sum(self):
        price = self.quantity * self.auto_item.kaina
        return price

    def pasirinkta_kategorija(self):
        cat = self.auto_item.auto_tipas.name
        return cat
    pasirinkta_kategorija.short_description = "kategorija"

    def __str__(self):
        return f'{self.uzsakymas_item.id}{self.auto_item.eurocode}, {self.quantity}, {self.price_sum}'


class Profilis(models.Model):
    """vartotojo klasė"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default='default.png', upload_to='profile_pics')

    class Meta:
        verbose_name_plural = "Profilis"

    def save(self, *args, **kwargs):
        """keičiamas nuotraukos dydis"""
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

    def __str__(self):
        return f'{self.user.username} profilis'

