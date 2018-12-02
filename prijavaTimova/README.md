# Aplikacija za prijavu timova

## Konkretni zahtevi

- Osigurano da tim mora da ima 3 ili 4 člana na backend-u.
- Otvoreni endpointovi za dovlačenje, izmenu i brisanje konkretnog člana.

## Dodatne funkcionalnosti

- Izmenjen dizajn sajta.
- Dodata internacionalizacija.
- Prilagođen sajt i za pristup preko mobilnih uređaja.
- Dodata mogućnost upload-ovanja slike za tim.
- Timu se automatski dodeljuje neka od default slika ako custom slika nije postavljena pri kreiranju.
- Dodata server-side validacija podataka.
- Dodati modal prozori koji obaveštavaju korisnika o uspehu ili greški pri kreiranju, ažuriranju i brisanju.
- Dodato statično hostovanje frontend-a.

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

Aplikaciji je sada aktivna na URL:

    http://localhost:5000

## REST struktura

| Endpoint            | Metoda | Opis                                                                         |
|---------------------|--------|------------------------------------------------------------------------------|
| `/api/teams/`       | GET    | Vraća sve timove.                                                             |
| `/api/teams/`       | POST   | Kreira novi tim. Očekuje `body` JSON strukture [Tim](#Tim).                                                              |
| `/api/teams/<uuid>` | GET    | Vraća tim čiji je UUID *uuid*.                                                |
| `/api/teams/<uuid>` | PUT    | Ažurira tim čiji je UUID *uuid*. Očekuje `body` JSON strukture [Tim](#Tim).                                              |
| `/api/teams/<uuid>` | DELETE | Briše tim čiji je UUID *uuid*.                                                |
| `/api/members/<id>` | GET    | Vraća člana čiji je ID *id*.                                                  |
| `/api/members/<id>` | PUT    | Ažurira člana čiji je ID *id*. Očekuje `body` JSON strukture [Član](#Član).                                                |
| `/api/members/<id>` | DELETE | Briše člana čiji je ID *id*.                                                  |
| `/api/secret/`      | GET    | Pristupanjem preko veb pretraživača aktivira tajni veb dizajn mod iz devedesetih. |

## JSON strukture podataka

### Tim

| Ključ          | Tip vrednosti | Opis                                                          |
|----------------|---------------|---------------------------------------------------------------|
| `name`         | `String`      | Naziv tima                                                    |
| `description`  | `String`      | Opis tima                                                     |
| `photo_url`    | `String`      | URL za fotografiju tima                                       |
| `team_members` | `Član[]`    | Niz članova koji pripadaju timu. Mora sadržati 3 ili 4 člana. |

### Član

| Ključ          | Tip vrednosti | Opis          |
|----------------|---------------|---------------|
| `first_name`   | `String`      | Ime           |
| `last_name`    | `String`      | Prezime       |
| `email`        | `String`      | Email         |
| `phone_number` | `String`      | Broj telefona |
| `school`       | `String`      | Škola         |
| `city`         | `String`      | Grad          |