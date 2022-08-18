from model import Kuharica, Kategorija, Recept

DATOTEKA_S_STANJEM = "stanje.json"

try:
    kuharica = Kuharica.preberi_iz_datoteke(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    kuharica = Kuharica()


DODAJ_KATEGORIJO = 1
POBRISI_KATEGORIJO = 2
PRIKAZI_KATEGORIJO = 3
DODAJ_RECEPT = 4
POBRISI_RECEPT = 5
DODAJ_SESTAVINO = 6
POBRISI_SESTAVINO = 7
IZHOD = 8


def preberi_stevilo():
    while True:
        vnos = input("> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")


def izberi_moznost(moznosti):
    for i, (_moznost, opis) in enumerate(moznosti, 1):
        print(f"{i}) {opis}")
    while True:
        i = preberi_stevilo()
        if 1 <= i <= len(moznosti):
            moznost, _opis = moznosti[i - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(moznosti)}.")


def prikaz_kategorije(kategorija):
    return f"{kategorija.ime}"


def prikaz_recepta(recept):
    return f"{recept.ime}, sestavine: {recept.sestavine}"


def prikaz_sestavine(sestavine):
    for sestavina in sestavine.keys():
        return f'{sestavina} - {sestavine[sestavina]}'


def izberi_kategorijo(model):
    return izberi_moznost([(kategorija, prikaz_kategorije(kategorija)) for kategorija in model.kategorije])


def izberi_recept(model):
    return izberi_moznost([(recept, prikaz_recepta(recept)) for recept in model.recepti])

def izberi_sestavino(recept):
    return izberi_moznost([(ime, prikaz_sestavine(recept.sestavine)) for ime in recept.sestavine.keys()])


def tekstovni_vmesnik():
    prikazi_pozdravno_sporocilo()
    while True:
        prikazi_aktualne_recepte()
        ukaz = izberi_moznost(
            [
                (DODAJ_KATEGORIJO, "dodaj novo kategorijo"),
                (POBRISI_KATEGORIJO, "pobriši kategorijo"),
                (PRIKAZI_KATEGORIJO, "prikaži kategorijo"),
                (DODAJ_RECEPT, "dodaj nov recept"),
                (POBRISI_RECEPT, "pobriši recept"),
                (DODAJ_SESTAVINO, "dodaj novo sestavino"),
                (POBRISI_SESTAVINO, "pobriši sestavino"),
                (IZHOD, "zapri program"),
            ]
        )
        if ukaz == DODAJ_KATEGORIJO:
            dodaj_kategorijo()
        elif ukaz == POBRISI_KATEGORIJO:
            pobrisi_kategorijo()
        elif ukaz == PRIKAZI_KATEGORIJO:
            prikazi_kategorijo()
        elif ukaz == DODAJ_RECEPT:
            dodaj_recept()
        elif ukaz == POBRISI_RECEPT:
            pobrisi_recept()
        elif ukaz == DODAJ_SESTAVINO:
            dodaj_sestavino()
        elif ukaz == POBRISI_SESTAVINO:
            pobrisi_sestavino()
        elif ukaz == IZHOD:
            kuharica.shrani_v_datoteko(DATOTEKA_S_STANJEM)
            print("Nasvidenje!")
            break


def prikazi_pozdravno_sporocilo():
    print("Pozdravljeni!")


def prikazi_aktualne_recepte():
    if kuharica.kategorije:
        for kategorija in kuharica.kategorije:
            for recept in kategorija.recepti:
                print(f"- {prikaz_recepta(recept)}")
    else:
        print("Ker nimate še nobene kategorije, morate eno ustvariti.")
        dodaj_kategorijo()


def dodaj_kategorijo():
    print("Vnesite podatke nove kategorije.")
    ime = input("Ime> ")
    nova_kategorija = Kategorija(ime, [])
    kuharica.dodaj_kategorijo(nova_kategorija)


def pobrisi_kategorijo():
    print("Izberite kategorijo, ki bi jo radi odstranili.")
    kategorija = izberi_kategorijo(kuharica)
    kuharica.pobrisi_kategorijo(kategorija)


def prikazi_kategorijo():
    print("Izberite kategorijo, ki bi jo radi videli.")
    kategorija = izberi_kategorijo(kuharica)
    return f'{kategorija} : {kategorija.recepti}'


def dodaj_recept():
    kategorija = izberi_kategorijo(kuharica)
    print("Vnesite podatke novega recepta.")
    sestavine = {}
    ime = input("Ime> ")
    while True:
        try:
            stevilo_oseb = int(input("Vnesite za koliko oseb je primeren recept> "))
            break
        except:
            print('Vnesti morate število!')
    while True:
        try:
            tezavnost = int(input("Težavnost, vnesite število od 1 do 5> "))
            break
        except:
            print('Vnesti morate število!')
    postopek = input("Postopek> ")
    nov_recept = Recept(ime, stevilo_oseb, sestavine, tezavnost, postopek)
    kategorija.dodaj_recept(nov_recept)


def pobrisi_recept():
    kategorija = izberi_kategorijo(kuharica)
    print("izberite recept, ki bi ga radi odstranili.")
    recept = izberi_recept(kategorija)
    kategorija.pobrisi_recept(recept)


def dodaj_sestavino():
    print('Izberite kategorijo kjer boste dodajali sestavino.')
    kategorija = izberi_kategorijo(kuharica)
    print("Izberite recept v katerega bi radi dodali sestavino.")
    recept = izberi_recept(kategorija)
    print("Vnesite podatke.")
    ime = input("Ime> ")
    kolicina = input("Količina> ")
    recept.dodaj_sestavino(ime, kolicina)


def pobrisi_sestavino():
    print('Izberite kategorijo kjer bi radi odstranili sestavino.')
    kategorija = izberi_kategorijo(kuharica)
    print("Izberite recept kjer bi radi odstrani sestavino.")
    recept = izberi_recept(kategorija)
    sestavina = izberi_sestavino(recept)
    recept.pobrisi_sestavino(sestavina)


tekstovni_vmesnik()





