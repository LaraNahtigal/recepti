import json

class Kuharica:
    def __init__(self):
        self.kategorije = []
        self.aktualna_kategorija = None

    def dodaj_kategorijo(self, kategorija):
        self.kategorije.append(kategorija)
        if not self.aktualna_kategorija:
            self.aktualna_kategorija = kategorija

    def pobrisi_kategorijo(self, kategorija):
        self.kategorije.remove(kategorija)

    def zamenjaj_kategorijo(self, kategorija):
        self.aktualna_kategorija = kategorija

    def dodaj_recept(self, recept):
        self.aktualna_kategorija.dodaj_recept(recept)

    def pobrisi_recept(self, recept):
        self.aktualna_kategorija.pobrisi_recept(recept)

    def v_slovar(self):
        return {
            "kategorije": [kategorija.v_slovar() for kategorija in self.kategorije],
            "aktualna_kategorija": self.kategorije.index(self.aktualna_kategorija)
            if self.aktualna_kategorija
            else None,
        }

    @staticmethod
    def iz_slovarja(slovar):
        kuharica = Kuharica()
        kuharica.kategorije = [
            Kategorija.iz_slovarja(nek_spisek) for nek_spisek in slovar["kategorije"]
        ]
        if slovar["aktualna_kategorija"] is not None:
            kuharica.aktualna_kategorija = kuharica.spiski[slovar["aktualna_kategorija"]]
        return kuharica

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
            return Kuharica.iz_slovarja(slovar)

    def preveri_podatke_nove_kategorije(self, ime):
        napake = {}
        if not ime:
            napake["ime"] = "Ime mora biti neprazno."
        for kategorija in self.kategorije:
            if kategorija.ime == ime:
                napake["ime"] = "Ime je že zasedeno."
        return napake

class Kategorija:
    def __init__(self, ime):
        self.ime = ime
        self.recepti = []
        self.aktualni_recept = None

    def dodaj_recept(self, recept):
        self.recepti.append(recept)
        if not self.aktualni_recept:
            self.aktualni_recept = recept

    def pobrisi_recept(self, recept):
        self.recepti.remove(recept)

    def zamenjaj_recept(self, recept):
        self.aktualni_recept = recept

    def stevilo_receptov(self):
        return len(self.recepti)

    def v_slovar(self):
        return {
            "ime": self.ime,
            "recepti": [
                recept.v_slovar() for recept in self.recepti
                ],
        }

    @staticmethod
    def iz_slovarja(slovar):
        kategorija = Kategorija(slovar["ime"])
        kategorija.recepti = [
            Recept.iz_slovarja(nek_recept) for nek_recept in slovar["recepti"]
        ]
        return kategorija

class Recept:
    def __init__(self, ime, stevilo_oseb, tezavnost, postopek):
        self.ime = ime
        self.stevilo_oseb = stevilo_oseb
        self.tezavnost = tezavnost
        self.sestavine = {}
        self.postopek = postopek
        
    def dodaj_sestavino(self, ime, kolicina):
        self.sestavine[ime] = kolicina

    def pobrisi_sestavino(self, ime):
        self.sestavine.pop(ime)

    def v_slovar(self):
        return {
            "ime": self.ime,
            "stevilo_oseb" : self.stevilo_oseb,
            "tezavnost": self.tezavnost,
            "sestavine": self.sestavine,
            "postopek": self.postopek
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Recept(
            slovar["ime"],
            slovar["stevilo_oseb"],
            slovar["tezavnost"],
            slovar["sestavine"],
            slovar["postopek"]
        )


