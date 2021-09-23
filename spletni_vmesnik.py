import bottle

from model import Kuharica, Kategorija, Recept

def nalozi_stanje(stanje):
    return Kuharica.preberi_iz_datoteke(stanje)

def shrani_stanje(stanje):
    ime_datoteke = "stanje.json"
    return stanje.shrani_v_datoteko(ime_datoteke)

@bottle.get("/")
def osnovna_stran():
    stanje = nalozi_stanje()
    return bottle.template(
        "osnovna_stran.html",
        recepti=stanje.aktualna_kategorija.recepti if stanje.aktualna_kategorija else [],
        kategorije=stanje.kategorije,
        aktualna_kategorija=stanje.aktualna_kategorija,
    )

@bottle.post("/dodaj/")
def dodaj_recept():
    ime = bottle.request.forms.getunicode("ime")
    stevilo_oseb = bottle.request.forms.getunicode("stevilo_oseb")
    tezavnost = bottle.request.forms.getunicode("tezavnost")
    postopek = bottle.request.forms.getunicode("postopek")
    recept = Recept(ime, stevilo_oseb, tezavnost, postopek)
    stanje = Kuharica.preberi_iz_datoteke()
    stanje.dodaj_recept(recept)
    shrani_stanje(stanje)
    bottle.redirect("/")

@bottle.post("/dodaj-sestavino/")
def dodaj_sestavino():
    ime = bottle.request.forms.getunicode("ime")
    kolicina = bottle.request.forms.getunicode("kolicina")
    recept = Kuharica.aktalna_kategorija.aktualni_recept
    recept.dodaj_sestavino(ime, kolicina)
    shrani_stanje(recept)
    

@bottle.get("/dodaj-kategorijo/")
def dodaj_kategorijo_get():
    return bottle.template("dodaj_kategorijo.html", napake={}, polja={})

@bottle.post("/dodaj-kategorijo/")
def dodaj_kategorijo_post():
    ime = bottle.request.forms.getunicode("ime")
    polja = {"ime": ime}
    stanje = nalozi_stanje()
    napake = stanje.preveri_podatke_nove_kategorije(ime)
    if napake:
        return bottle.template("dodaj_kategorijo.html", napake=napake, polja=polja)
    else:
        kategorija = Kategorija(ime)
        stanje.dodaj_kategorijo(kategorija)
        shrani_stanje(stanje)
        bottle.redirect("/")

@bottle.post("/zamenjaj-aktualni-spisek/")
def zamenjaj_aktualno_kategorijo():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    stanje = nalozi_stanje()
    kategorija = stanje.kategorije[int(indeks)]
    stanje.aktualna_kategorija = kategorija
    shrani_stanje(stanje)
    bottle.redirect("/")

@bottle.post("/zamenjaj-aktualni-recept/")
def zamenjaj_aktualni_recept():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    stanje = nalozi_stanje()
    recept = stanje.aktualna_kategorija.recept[int(indeks)]
    stanje.aktualna_kategorija.aktualni_recept = recept
    shrani_stanje(stanje)
    bottle.redirect("/")

@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"
  
bottle.run(reloader=True, debug=True)
