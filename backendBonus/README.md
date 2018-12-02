# Backend za rezervaciju avio-karata

Ovu aplikaciju prati već popunjena baza podataka radi bržeg testiranja funkcionalnosti. Pri rezervisanju letova, jedina informacija koju naša implementacija zahteva je ime osobe koja rezerviše. Ovo je radi jednostavnosti, jer kreiranje modela za korisnika nije bio fokus.

## Uputstvo za korišćenje

Komande se izvršavaju unutar foldera aplikacije:

    cd backendBonus

Instaliranje virtuelnog okruženja (sa pretpostavkom da je `virtualenv` već instaliran globalno koristeći `pip install virtualenv`):

    virtualenv venv

Pokretanje virtuelnog okruženja:

    Windows: <putanja do projekta>\venv\Scripts\activate.bat
    Linux: source venv/bin/activate

Instaliranje neophodnih biblioteka:

    pip install -r requirements.txt

Pokretanje aplikacije:

    python app.py
    
Pokretanje aplikacije u debug modu:

    python app.py debug

Aplikacija je sada aktivna na URL:

    http://localhost:5000

## Funkcionalnosti

- Omogućen pristup svim letovima u bazi podataka.
- Filtriranje letova na osnovu polaznog tačke, krajnje tačke i/ili datuma leta.
- Pristupanje informacija o izvesnom letu na osnovu *id*-a.
- Rezervisanje letova samo ako postoje slobodna mesta na njemu.

## REST struktura

| Endpoint           | Metoda | Opis                                                                                                                                                                                                           |
|--------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/api/flight/`     | GET    | Vraća sve letove. Moguće je filtriranje letova koristeći query parametara `start_city`, `finish_city` i `date`. Pružanje bilo koje kombinacije ova 3 parametara filtrira letove koji bivaju vraćeni korisniku. |
| `/api/flight/<id>` | GET    | Vraća let čiji je ID *id*.                                                                                                                                                                                      |
| `/api/flight/<id>` | POST   | Rezerviše let čiji je ID *id* ako ima slobodnih mesta, u suprotnom vraća grešku. Očekuje `body` JSON oblika sa ključem `name` koji sadrži ime osobe koja rezerviše let.                                             |

