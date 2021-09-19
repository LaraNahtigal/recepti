from model import Kuharica, Kategorija, Recept

DATOTEKA_S_STANJEM = "stanje.json"

try:
    kuharica = Kuharica.preberi_iz_datoteke(DATOTEKA_S_STANJEM)
except FileNotFoundError:
    kuharica = Kuharica()


DODAJ_KATEGORIJO = 1
POBRISI_KATEGORIJO = 2
ZAMENJAJ_KATEGORIJO = 3
DODAJ_RECEPT = 4
POBRISI_RECEPT = 5
IZHOD = 6


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
    vsa = kategorija.stevilo_vseh()
    return f"{kategorija.ime} ({vsa})"


def prikaz_recepta(recept):
    return f"{recept.ime}"


def izberi_kategorijo(model):
    return izberi_moznost([(kategorija, prikaz_kategorije(kategorija)) for kategorija in model.kategorije])


def izberi_recept(model):
    return izberi_moznost(
        [
            (recept, prikaz_recepta(recept))
            for recept in model.kategorija.recepti
        ]
    )


def tekstovni_vmesnik():
    prikazi_pozdravno_sporocilo()
    while True:
        prikazi_aktualne_recepte()
        ukaz = izberi_moznost(
            [
                (DODAJ_KATEGORIJO, "dodaj novo kategorijo"),
                (POBRISI_KATEGORIJO, "pobriši kategorijo"),
                (ZAMENJAJ_KATEGORIJO, "prikaži drugo kategorijo"),
                (DODAJ_RECEPT, "dodaj nov recept"),
                (POBRISI_RECEPT, "pobriši recept"),
                (IZHOD, "zapri program"),
            ]
        )
        if ukaz == DODAJ_KATEGORIJO:
            dodaj_kategorijo()
        elif ukaz == POBRISI_KATEGORIJO:
            pobrisi_kategorijo()
        elif ukaz == ZAMENJAJ_KATEGORIJO:
            zamenjaj_kategorijo()
        elif ukaz == DODAJ_RECEPT:
            dodaj_recept()
        elif ukaz == POBRISI_RECEPT:
            pobrisi_recept()
        elif ukaz == IZHOD:
            kuharica.shrani_v_datoteko(DATOTEKA_S_STANJEM)
            print("Nasvidenje!")
            break


def prikazi_pozdravno_sporocilo():
    print("Pozdravljeni!")


def prikazi_aktualne_recepte():
    if kuharica.aktualna_kategorija:
        for recept in kuharica.aktualna_kategorija.recepti:
            print(f"- {prikaz_recepta(recept)}")
    else:
        print("Ker nimate še nobene kategorije, morate eno ustvariti.")
        dodaj_kategorijo()


def dodaj_kategorijo():
    print("Vnesite podatke nove kategorije.")
    ime = input("Ime> ")
    nova_kategorija = Kategorija(ime)
    kuharica.dodaj_kategorijo(nova_kategorija)


def pobrisi_kategorijo():
    kategorija = izberi_kategorijo(kuharica)
    kuharica.pobrisi_kategorijo(kategorija)


def zamenjaj_kategorijo():
    print("Izberite kategorijo, na katero bi preklopili.")
    kategorija = izberi_kategorijo(kuharica)
    kuharica.zamenjaj_kategorijo(kategorija)


def dodaj_recept():
    print("Vnesite podatke novega recepta.")
    ime = input("Ime> ")
    tezavnost = input("Tezavnost> ")
    sestavine = input("Sestavine> ")
    postopek = input("Postopek> ")
    nov_recept = Recept(ime, tezavnost, sestavine, postopek)
    kuharica.dodaj_recept(nov_recept)


def pobrisi_recept():
    recept = izberi_recept(kuharica)
    kuharica.pobrisi_recept(recept)


tekstovni_vmesnik()





