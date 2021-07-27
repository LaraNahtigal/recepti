DODAJ_SPISEK = 1
POBRISI_SPISEK = 2
ZAMENJAJ_SPISEK = 3
DODAJ_RECEPT = 4
POBRISI_RECEPT = 5
OCENI_RECEPT = 6
IZHOD = 7

def tekstovni_vmesnik():
    prikazi_pozdravno_sporocilo()
    while True:
        prikazi_aktualne_recepte()
        ukaz = izberi_moznost ([
            (DODAJ_SPISEK, "dodaj nov spisek"),
            (POBRISI_SPISEK, "pobriši spisek"),
            (ZAMENJAJ_SPISEK, "prikaži drug spisek"),
            (DODAJ_RECEPT, "dodaj nov recept"),
            (POBRISI_RECEPT, "pobriši recept"),
            (OCENI_RECEPT, "oceni recept"),
            (IZHOD, "zapri program"),
        ])
        if ukaz == DODAJ_SPISEK:
            dodaj_spisek()
        elif ukaz == POBRISI_SPISEK:
            pobrisi_spisek()
        elif ukaz == ZAMENJAJ_SPISEK:
            zamenjaj_spisek()
        elif ukaz == DODAJ_RECEPT:
            dodaj_recept()
        elif ukaz == POBRISI_RECEPT:
            pobrisi_recept()
        elif ukaz == OCENI_RECEPT:
            oceni_recept()
        elif ukaz == izhod:
            print('Nasvidenje!')
            break