class Model:
    def __init__(self):
        self.spiski = []

    def dodaj_spisek(self, spisek):
        self.spiski.append(spisek)
        
class Spisek:
    def __init__(self, ime):
        self.ime = ime
        self.recepti = []

    def dodaj_recept(self, recept):
        self.recepti.append(recept)

    def stevilo_receptov(self):
        stevilo = 0
        for recept in self.recepti:
            stevilo += 1
        return stevilo


class Recept:
    def __init__(self, ime, recept, težavnost):
        self.ime = ime
        self.recept = recept
        self.težavnost = težavnost
        self.ocenjeno = False 

    def oceni(self):
        self.ocenjeno = True

