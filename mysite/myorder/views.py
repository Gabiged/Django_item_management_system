import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Q
from .forms import UserUpdateForm, ProfilisUpdateForm
from .models import Auto, Kategorija, Likutis, Uzsakymas, UzsakymoEilute
from django.views import generic
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .tables import AutoTable
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)


def index(request):
    """f-ja skaičiuojanti sandėlio pozicijas ir likučius"""
    num_autos = Auto.objects.count()
    num_categ = Kategorija.objects.all().count()
    visi = [e for e in Kategorija.objects.annotate(aut_count=Count('kategorijos')).values('aut_count')]
    num_categ_leng = list(visi[0].values())[0]
    num_categ_mikr = list(visi[1].values())[0]
    num_categ_sunk = list(visi[2].values())[0]
    num_lik = list(Likutis.objects.aggregate(Sum('kiekis')).values())[0]
    logger.warning(request.session.keys())
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    kontext = {
        'num_autos': num_autos,
        'num_categ': num_categ,
        'num_categ_leng': num_categ_leng,
        'num_categ_mikr': num_categ_mikr,
        'num_categ_sunk': num_categ_sunk,
        'num_lik': num_lik,
        'num_visits': num_visits
    }
    return render(request, 'index.html', context=kontext)


class AutoListView(generic.ListView):
    """klasė pateikianti visų prekių sąrašą"""
    model = Auto
    table_class = AutoTable
    template_name = 'auto_list.html'


class UzsakymasListView(LoginRequiredMixin, ListView):
    """ klasė, kad rodytų tik vartotojo uzsakymų sąrašą """
    model = Uzsakymas
    context_object_name = 'uzsakymai'
    template_name = "uzsakymas_list.html"
    paginate_by = 10

    def get_queryset(self):
        """f-ja, kad vartotojo užsakymai būtų išrūšiuoti pagal užsakymo atlikimo datą"""
        return Uzsakymas.objects.filter(pirkejas=self.request.user).order_by('due_back')

class UzsakymasDetailView(LoginRequiredMixin, DetailView):
    """klasė kiekvieno užsakymo detalizavimui"""
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'

    def get_success_url(self):
        return reverse('uzsakymas-detail', kwargs={'pk': self.object.id})


def categories(request):
    return {'categories': Kategorija.objects.all()}

def search(request):
    """paieškos lauko f-ja"""
    query_text = request.GET.get('query_text')
    search_results = Auto.objects.filter(Q(eurocode__icontains=query_text) | Q(pavadinimas__icontains=query_text))
    return render(request, 'search.html', {"auto": search_results, "query_text": query_text})

@csrf_protect
def register(request):
    """Vartotojo registravimo funkcija"""
    if request.method == 'POST':
        # imame is uzpildytos formos reiksmes
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        fields = [username, email, password, password2]
        if all(fields):
            """tikriname ar sutampa passwordai"""
            if password == password2:
                """tikriname, ar neuzimtas username"""
                if User.objects.filter(username=username).exists():
                    messages.error(request, f"Username already exist! {username}")
                    return redirect("register")
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, f"Email already exists! {email}")
                        return redirect("register")
                    else:
                        """jeigu viskas patikrinta, registruojam nauja vartotoja"""
                        User.objects.create_user(username=username, email=email, password=password)
                        messages.success(request, f"User name created {username}")
            else:
                messages.error(request, 'Passwords do not match!')
                return redirect("register")
        else:
            """pranesama, jei bandoma registuotis neuzpildzius reikalaujamų laukų"""
            messages.error(request, "Please fill all fields!")
            return redirect("register")
    return render(request, 'register.html')


@login_required
def profilis(request):
    """profilis gali buti keiciamas tik prisijungus"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile reniewed")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profilis.html', context)
