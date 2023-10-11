# Importeer de benodigde functies
from random import randint


# Maak de Blackjack-klasse, die alle spelfuncties en attributen zal bevatten
class Blackjack():
    def __init__(self):
        self.deck = []  # ingesteld op een lege lijst
        self.soorten = ("Schoppen", "Harten", "Ruiten", "Klaveren")
        self.waardes = (2, 3, 4, 5, 6, 7, 8, 9, 10, 'Boer', 'Vrouw', 'Heer', 'Aas')

    # Maak een methode die een deck van 52 kaarten maakt, elke kaart moet een tuple zijn met een waarde en soort
    def maakDeck(self):
        for soort in self.soorten:
            for waarde in self.waardes:
                self.deck.append((waarde, soort))  # bv: (7, "Harten")

    # Methode om een kaart uit het deck te halen met een willekeurige indexwaarde
    def trekKaart(self):
        return self.deck.pop(randint(0, len(self.deck) - 1))


# Maak een klasse voor de speler en dealer objecten
class Speler():
    def __init__(self, naam):
        self.naam = naam
        self.hand = []
        self.geld = 500

    def krijgGeld(self):
        return self.geld

    def stelGeldIn(self, bedrag, gewonnen):

            # Neem een bedrag om toe te voegen of af te trekken, de gewonnen parameter zal
            # bepalen of de speler heeft gewonnen en of het moet worden toegevoegd of afgetrokken.

        if gewonnen:
            self.geld += bedrag
        elif not gewonnen:
            self.geld -= bedrag

    # Neem een tuple en voeg het toe aan de hand
    def voegKaartToe(self, kaart):
        self.hand.append(kaart)

    def nieuwRonde(self):
        self.hand.clear()

    # Als het niet de beurt van de dealer is, laat dan slechts één van zijn kaarten zien, anders laat alle kaarten zien
    def zieHand(self, dealer_start=True):
        print(f"\n{self.naam}\n===========")


        for i in range(len(self.hand)):
            if self.naam == 'Dealer' and i == 0 and dealer_start:
                print("- of -")  # eerste kaart verbergen
            else:
                kaart = self.hand[i]
                print(f"{kaart[0]} van {kaart[1]}")
        print(f"Totaal = {self.berekenHand(dealer_start)}")

    # Als het niet de beurt van de dealer is, geef dan alleen het totaal van de tweede kaart terug
    def berekenHand(self, dealer_start=True):
        totaal = 0
        azen = 0  # bereken azen later
        kaart_waarden = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 'Boer': 10, 'Vrouw': 10,
                         'Heer': 10, 'Aas': 11}

        if self.naam == 'Dealer' and dealer_start:
            kaart = self.hand[1]
            return kaart_waarden[kaart[0]]

        for kaart in self.hand:
            if kaart[0] == 'Aas':
                azen += 1
            else:
                totaal += kaart_waarden[kaart[0]]

        for i in range(azen):
            if totaal + 11 > 21:
                totaal += 1
            else:
                totaal += 11

        return totaal


spel = Blackjack()
spel.maakDeck()


naam = input("Wat is jouw naam? ")
speler = Speler(naam)
dealer = Speler("Dealer")

while True:
    # Vraag de speler hoeveel ze willen inzetten
    inzet = 0
    print(f'Je hebt €{speler.krijgGeld()}. ')

    while inzet == 0 or speler.krijgGeld() - inzet < 0:
     # Behandel het verkrijgen en omzetten van de inzet
        try:
            inzet = int(input("Hoeveel wil je inzetten? "))

            # Als de inzet te hoog is, druk dan een bericht af
            if speler.krijgGeld() - inzet < 0:
                print("Sorry, je hebt niet zoveel geld. Probeer opnieuw!")
        except:
            print('Er is iets misgegaan, probeer het opnieuw!')

    # Voeg twee kaarten toe aan de hand van de dealer en de speler
    for i in range(2):
        speler.voegKaartToe(spel.trekKaart())
        dealer.voegKaartToe(spel.trekKaart())

    # Laat beide handen zien met behulp van de methode
    speler.zieHand()
    dealer.zieHand()

    speler_bust = False

    while input('Wil je blijven of kaart trekken? ').lower() != 'blijven':

        # Trek een kaart en voeg deze toe aan de hand van de speler
        speler.voegKaartToe(spel.trekKaart())

        # Laat beide handen zien met behulp van de methode
        speler.zieHand()
        dealer.zieHand()

        # Controleer of de speler boven de 21 is
        if speler.berekenHand() > 21:
            speler_bust = True
            break

    # Afhandeling van de beurt van de dealer, alleen uitvoeren als de speler niet over de 21 is gegaan
    dealer_bust = False

    if not speler_bust:
        while dealer.berekenHand(False) < 17:
            # Trek een kaart en voeg deze toe aan de hand van de dealer
            dealer.voegKaartToe(spel.trekKaart())

            # Controleer of de dealer boven de 21 is
            if dealer.berekenHand(False) > 21:
                dealer_bust = True
                break


    # Laat beide handen zien met behulp van de methode
    speler.zieHand()
    dealer.zieHand(False)

    # Bepaal een winnaar
    if speler_bust:
        print('Je bent boven de 21, beter geluk volgende keer!')
        speler.stelGeldIn(inzet, False)
    elif dealer_bust:
        print('De dealer is boven de 21, jij wint!')
        speler.stelGeldIn(inzet, True)
    elif dealer.berekenHand(False) > speler.berekenHand():
        print('De dealer heeft hogere kaarten, je verliest!')
        speler.stelGeldIn(inzet, False)
    elif dealer.berekenHand(False) < speler.berekenHand():
        print('Je verslaat de dealer, gefeliciteerd!')
        speler.stelGeldIn(inzet, True)
    else:
        print('Het is een push, niemand wint!')

    print(f'Je eindigt met €{speler.krijgGeld()}.')

    opnieuw = input("Wilt u doorgaan? (ja/nee) ").lower()
    if opnieuw == "ja":
        speler.nieuwRonde()
        dealer.nieuwRonde()
        continue
    if opnieuw == "nee":
        break
    else:
        print("ongeldige invoer. Alleen (ja/nee) invullen ")
    # Einde van het spel.
