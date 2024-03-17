import requests
from bs4 import BeautifulSoup

URL = {
    'blic': 'https://www.blic.rs/',
    'telegraf': 'https://www.telegraf.rs/',
    'danas': 'https://www.danas.rs/',
    'kurir': 'https://www.kurir.rs/',
    'nova': 'https://nova.rs/',
    '*': None
}

def uprosti(tekst):
    """ Uprošćava prosleđen string radi optimizacije pretrage.
    Parametar: tekst (string)
    Vraća: tekst (string)
    """
    zamena = {'č': 'c', 'ć': 'c', 'š': 's', 'đ': 'dj', 'ž': 'z'}
    tekst = tekst.lower()
    tekst = ''.join([zamena[slovo] if slovo in zamena else slovo for slovo in tekst])
    return tekst

def poklapanje(naslov, pretraga):
    """ Proverava da li se pretraga poklapa sa datim naslovom.
    Parametri: naslov (string), pretraga (string)
    Vraća: True/False (bool)
    """
    naslov = uprosti(naslov)
    if len(pretraga) > 4:
        pretraga = pretraga[:-1]
    if pretraga in naslov:
        return True
    else:
        return False
    
def napravi_supu(ime_portala):
    """ Pravi BeautifulSoup objekat na osnovu datog naziva portala.
    Parametar: ime_portala (string)
    Vraća: supa (BeautifulSoup objekat)
    """
    adresa = URL[ime_portala]
    sajt = requests.get(adresa)
    supa = BeautifulSoup(sajt.content, 'html.parser')
    return supa

def prikazi_rezultate(rezultati):
    """ Ispisuje rerezultate pretrage u konzoli.
    Parametar: rezultati (list)
    Vraća: (None)
    """
    print(f'\nRezultati ({len(naslovi_i_linkovi)})')
    for podaci in rezultati:
        print('\n', end='')
        print(podaci[0])
        print(podaci[1])
        
def moze(naslov):
    """ Proverava da li dati naslov može da se doda u listu.
    Parametar: naslov (string)
    Vraća: True/False (bool)
    """
    if poklapanje(naslov, pretraga):
        if naslov not in [x[0] for x in naslovi_i_linkovi]:
            return True
    return False
        
def dodaj(naslov, link):
    """ Dodaje dati naslov i link na kraj liste rezultata.
    Parametri: naslov (string), link (string)
    Vraća: (None)
    """
    global naslovi_i_linkovi
    naslovi_i_linkovi.append((naslov, link))

def pretrazi_blic():
    """ Koristeći BeautifulSoup funkcionalnosti pretražuje sajt Blica.
    Parametar: (None)
    Vraća: (None)
    """
    supa = napravi_supu('blic')
    vesti = supa.find_all('div', class_='news__content')
    for i in vesti:
        vest = i.find('a')
        naslov = vest.text.strip()
        link = vest['href']
        if moze(naslov):
            dodaj(naslov, link)
    
def pretrazi_telegraf():
    """ Koristeći BeautifulSoup funkcionalnosti pretražuje sajt Telegrafa.
    Parametar: (None)
    Vraća: (None)
    """
    supa = napravi_supu('telegraf')
    pretraga1 = supa.find_all('div', class_='page-content')
    for i in pretraga1:
        vesti = i.find_all('figcaption')
        for j in vesti:
            vest = j.a
            try:
                naslov = vest['title']
                link = vest['href']
                if moze(naslov):
                    dodaj(naslov, link)
            except:
                pass
            
def pretrazi_danas():
    """ Koristeći BeautifulSoup funkcionalnosti pretražuje sajt Danasa.
    Parametar: (None)
    Vraća: (None)
    """
    supa = napravi_supu('danas')
    vesti = supa.find_all('article', class_='post')
    for i in vesti:
        vest = i.find('h3').a
        naslov = vest.text.strip()
        link = vest['href']
        if moze(naslov):
            dodaj(naslov, link)

def pretrazi_kurir():
    """ Koristeći BeautifulSoup funkcionalnosti pretražuje sajt Kurira.
    Parametar: (None)
    Vraća: (None)
    """
    supa = napravi_supu('kurir')
    pretraga1 = supa.find('div', class_='mainContent')
    vesti = pretraga1.find_all('h2', class_='title')
    for i in vesti:
        vest = i.a
        naslov = vest.text.strip()
        link = vest['href']
        if moze(naslov):
            dodaj(naslov, link)
            
def pretrazi_novu():
    """ Koristeći BeautifulSoup funkcionalnosti pretražuje sajt Nove.
    Parametar: (None)
    Vraća: (None)
    """
    supa = napravi_supu('nova')
    vesti = supa.find_all('div', class_='uc-post-title')
    for i in vesti:
        vest = i.a
        naslov = vest.text.strip()
        link = vest['href']
        if moze(naslov):
            dodaj(naslov, link)

print('Dobro došli!')
print('Ovaj program omogućava pretragu vesti sa onlajn portala (Blic, Telegraf, Danas, Kurir, Nova). Prilikom pretrage, koristite ošišanu latinicu.')

izbor_portala = input('Unesite izvore koje želite da pretražujete, odvojene zarezom ili unesite * za pretragu svakog od portala: ').split(',')
izbor_portala = [portal.lower().strip() for portal in izbor_portala]

while True:
    naslovi_i_linkovi = []
    pretraga = input('\nUnesite izraz za pretragu: ').lower().strip()
    
    for portal in izbor_portala:
        if portal in URL:
            if portal == 'blic':
                pretrazi_blic()
            elif portal == 'telegraf':
                pretrazi_telegraf()
            elif portal == 'danas':
                pretrazi_danas()
            elif portal == 'kurir':
                pretrazi_kurir()
            elif portal == 'nova':
                pretrazi_novu()
            elif portal == '*':
                pretrazi_blic()
                pretrazi_telegraf()
                pretrazi_danas()
                pretrazi_kurir()
                pretrazi_novu()
   
    if naslovi_i_linkovi == []:
        print('\nNema rezultata')
    else:
        prikazi_rezultate(naslovi_i_linkovi)
        
    izbor = input('\nDa li želite nastaviti pretraživanje? (d/n) ')
    if izbor != 'd':
        break
    
print('\nKraj rada...')