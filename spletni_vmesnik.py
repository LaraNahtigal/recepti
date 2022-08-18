import bottle

from model import Kuharica, Kategorija, Recept, Uporabnik


UPORABNISKO_IME = "uporabnisko_ime"
SECRET = "To je skrivnost"


def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()


def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        UPORABNISKO_IME, secret=SECRET)
    if uporabnisko_ime:
        return Uporabnik.iz_datoteke(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.redirect("/registracija/")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SECRET)
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template("prijava.html", napaka=e.args[0])

        
@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)


@bottle.post("/registracija/")
def registracija_post():
    ime = bottle.request.forms.getunicode("ime")
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.registracija(ime, uporabnisko_ime, geslo_v_cistopisu)
        bottle.response.set_cookie(
            UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SECRET)
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template("registracija.html", napaka=e.args[0])


@bottle.get("/odjava/")
def odjava():
    bottle.response.delete_cookie(UPORABNISKO_IME, path="/")
    bottle.redirect("/prijava/")

######################################################################################################3

@bottle.get("/")
def zacetna_stran():
    uporabnik = trenutni_uporabnik()
    return bottle.template("osnovna_stran.html", kategorije = uporabnik.kuharica.kategorije)


@bottle.get("/kategorija/<index_kategorije:int>/")
def prikazi_kategorijo(index_kategorije):
    uporabnik = trenutni_uporabnik()
    kategorija = uporabnik.kuharica.kategorije[index_kategorije]
    return bottle.template(
        "kategorija.html",
        kategorije=uporabnik.kuharica.kategorije,
        aktualna_kategorija=kategorija,
        index_aktualne_kat=index_kategorije,
        recepti=uporabnik.kuharica.kategorije[index_kategorije].recepti
    )


@bottle.get("/dodaj_kategorijo/")
def dodaj_kategorijo_get():
    return bottle.template(
        "dodaj_kategorijo.html", napake={}, polja={}
    )


@bottle.post("/dodaj_kategorijo/")
def dodaj_kategorijo_post():
    uporabnik = trenutni_uporabnik()
    ime = bottle.request.forms.getunicode("ime_kategorije")
    kategorija = Kategorija(ime, recepti=[])
    napake = uporabnik.kuharica.preveri_podatke_nove_kategorije(kategorija)
    if napake:
        polja = {"ime": ime}
        return bottle.template("dodaj_kategorijo.html", napake=napake, polja=polja)
    else:
        uporabnik.kuharica.dodaj_kategorijo(ime)
        shrani_stanje(uporabnik)
        bottle.redirect("/")


@bottle.post("/odstrani_kategorijo/")
def odstrani_kategorijo():
    uporabnik = trenutni_uporabnik()
    odstranjena = bottle.request.forms.getunicode("ime")
    for neka_kategorija in uporabnik.kuharica.kategorije:
        if neka_kategorija.ime == odstranjena:
            uporabnik.kuharica.pobrisi_kategorijo(odstranjena)
        else:
            continue
    shrani_stanje(uporabnik)
    bottle.redirect("/")


@bottle.post("/dodaj_recept/<index_kategorije:int>/")
def dodaj_recept(index_kategorije):
    uporabnik = trenutni_uporabnik()
    ime = bottle.request.forms.getunicode("ime")
    stevilo_oseb = int(bottle.request.forms.getunicode("stevilo_oseb"))
    tezavnost = int(bottle.request.forms.getunicode("tezavnost"))
    sestavine = {}
    postopek = bottle.request.forms.getunicode("postopek")
    uporabnik.kuharica.kategorije[index_kategorije].dodaj_recept(ime, stevilo_oseb, tezavnost, sestavine, postopek)
    shrani_stanje(uporabnik)
    bottle.redirect(f"/kategorija/{index_kategorije}/")


@bottle.post("/odstrani_recept/<index_kategorije:int>/")
def odstrani_recept(index_kategorije):
    uporabnik = trenutni_uporabnik()
    odstranjen = bottle.request.forms.getunicode("ime")
    kategorija = uporabnik.kuharica.kategorije[index_kategorije]
    for recept in kategorija.recepti:
        if recept.ime == odstranjen:
            uporabnik.kuharica.kategorije[index_kategorije].pobrisi_recept(odstranjen)
        else:
            continue
    shrani_stanje(uporabnik)
    bottle.redirect(f"/kategorija/{index_kategorije}/")   
    

@bottle.get("/recept/<index_kategorije:int>/<index_recepta:int>/")
def prikazi_recept(index_kategorije, index_recepta):
    uporabnik = trenutni_uporabnik()
    kategorija = uporabnik.kuharica.kategorije[index_kategorije]
    recept = uporabnik.kuharica.kategorije[index_kategorije].recepti[index_recepta]
    return bottle.template(
        "recept.html",
        kategorije=uporabnik.kuharica.kategorije,
        aktualna_kategorija=kategorija,
        recepti=uporabnik.kuharica.kategorije[index_kategorije].recepti,
        aktualen_recept=recept,
        index_aktualnega_rec=index_recepta,
        index_aktualne_kat = index_kategorije,
        sestavine=uporabnik.kuharica.kategorije[index_kategorije].recepti[index_recepta].sestavine
    )


@bottle.post("/dodaj_sestavino/<index_kategorije:int>/<index_recepta:int>/")
def dodaj_sestavino(index_kategorije, index_recepta):
    uporabnik = trenutni_uporabnik()
    ime = bottle.request.forms.getunicode("ime")
    kolicina = bottle.request.forms.getunicode("kolicina")
    uporabnik.kuharica.kategorije[index_kategorije].recepti[index_recepta].dodaj_sestavino(ime, kolicina)
    shrani_stanje(uporabnik)
    bottle.redirect(f"/recept/{index_kategorije}/{index_recepta}/")


@bottle.post("/odstrani_sestavino/<index_kategorije:int>/<index_recepta:int>/")
def odstrani_sestavino(index_kategorije, index_recepta):
    uporabnik = trenutni_uporabnik()
    ime = bottle.request.forms.getunicode("ime")
    for ime_sestavine in list(uporabnik.kuharica.kategorije[index_kategorije].recepti[index_recepta].sestavine.keys()):
        if ime == ime_sestavine:
            uporabnik.kuharica.kategorije[index_kategorije].recepti[index_recepta].odstrani_sestavino(ime)
        else:
            continue
    shrani_stanje(uporabnik)
    bottle.redirect(f"/recept/{index_kategorije}/{index_recepta}/") 
    
    
@bottle.get('/img/<picture>')
def serve_picture(picture):
    return bottle.static_file(picture, root='img')


@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"
  
  
bottle.run(reloader=True, debug=True)
