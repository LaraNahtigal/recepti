import json
import random
import hashlib

class Kuharica:
    def __init__(self, kategorije):
        self.kategorije = kategorije

    def dodaj_kategorijo(self, ime_kategorije):
        for kategorija in self.kategorije:
            if kategorija.ime == ime_kategorije:
                return {"ime": "Kategorija s tem imenom že obstaja"}
        nova_kategorija = Kategorija(ime_kategorije, recepti = [])
        self.kategorije.append(nova_kategorija)
    

    def pobrisi_kategorijo(self, kategorija):
        for neka_kategorija in self.kategorije:
            if neka_kategorija.ime == kategorija:
                self.kategorije.remove(neka_kategorija)


    def preveri_podatke_nove_kategorije(self, nova_kategorija):
        for kategorija in self.kategorije:
            if kategorija.ime == nova_kategorija.ime:
                return {"ime": "Kategorija s tem imenom že obstaja"}

    def recepti_v_kategoriji(self, kategorija):
        for kategorija in self.kategorije:
            return kategorija.recepti


    def v_slovar(self):
        return {
            "kategorije": [kategorija.v_slovar() for kategorija in self.kategorije]
        }

    @staticmethod
    def iz_slovarja(slovar):
        kuharica = Kuharica(
            [
            Kategorija.iz_slovarja(nek_spisek) for nek_spisek in slovar["kategorije"]
            ]
        )
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


class Kategorija:
    def __init__(self, ime, recepti):
        self.ime = ime
        self.recepti = recepti


    def dodaj_recept(self, recept, stevilo_oseb, tezavnost, sestavine, postopek):
        for nek_recept in self.recepti:
            if nek_recept.ime == recept:
                return {"ime": "Recept s tem imenom že obstaja"}
        nov_recept = Recept(recept, stevilo_oseb, tezavnost, sestavine, postopek)
        self.recepti.append(nov_recept)


    def pobrisi_recept(self, recept):
        for nek_recept in self.recepti:
            if nek_recept.ime == recept:
                self.recepti.remove(nek_recept)


    def v_slovar(self):
        return {
            "ime": self.ime,
            "recepti": [
                recept.v_slovar() for recept in self.recepti
                ],
        }


    @staticmethod
    def iz_slovarja(slovar):
        kategorija = Kategorija(slovar["ime"], [Recept.iz_slovarja(recept) for recept in slovar["recepti"]],)
        return kategorija


class Recept:
    def __init__(self, ime, stevilo_oseb, tezavnost, sestavine, postopek):
        self.ime = ime
        self.stevilo_oseb = stevilo_oseb
        self.tezavnost = tezavnost
        self.sestavine = sestavine
        self.postopek = postopek
        

    def dodaj_sestavino(self, ime, kolicina):
        self.sestavine[ime] = kolicina


    def odstrani_sestavino(self, ime):
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


class Uporabnik:

    def __init__(self, ime, uporabnisko_ime, zasifrirano_geslo, kuharica):
        self.ime = ime
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.kuharica = kuharica


    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"


    @staticmethod
    def iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None


    def preveri_geslo(self, geslo_v_cistopisu):
        sol, _ = self.zasifrirano_geslo.split("$")
        return self.zasifrirano_geslo == Uporabnik._zasifriraj_geslo(geslo_v_cistopisu, sol)


    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabnik = Uporabnik.iz_datoteke(uporabnisko_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja!")
        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
            return uporabnik
        else:
            raise ValueError("Geslo je napačno!")


    @staticmethod
    def registracija(ime, uporabnisko_ime, geslo_v_cistopisu):
        if Uporabnik.iz_datoteke(uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja!")
        else:
            kategorije = []
            zasifrirano_geslo = Uporabnik._zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Uporabnik(ime, uporabnisko_ime, zasifrirano_geslo, Kuharica(kategorije))
            uporabnik.v_datoteko()
            return uporabnik


    def _zasifriraj_geslo(geslo_v_cistopisu, sol=None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posoljeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posoljeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"


    def v_datoteko(self):
        with open(Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w", encoding="utf-8") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)


    def v_slovar(self):
        return {
            "ime": self.ime,
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "kuharica": self.kuharica.v_slovar()
        }


    @staticmethod
    def iz_slovarja(slovar):
        ime = slovar["ime"]
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        kuharica = Kuharica.iz_slovarja(slovar["kuharica"])
        return Uporabnik(ime, uporabnisko_ime, zasifrirano_geslo, kuharica)