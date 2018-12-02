# Teorija

1. Objasniti razliku između `POST` i `PUT` metode.

U RESTful dizajnu `POST` se koristi za dodavanje novih resursa, dok se `PUT` koristi za ažuriranje već postojećih resursa.

2. Klijent je serveru poslao zahtev sa XML body-jem, a server očekuje JSON. Koji će biti statusni kod u odgovoru servera?

Server će poslati `400 BAD REQUEST` status.

3. Šta je to API?

API je skraćenica od Aplikacioni Programski Interfejs i predstavlja način komuniciranja između dva nezavisna programa. Na primer, kada klijent zahteva podatke od servera sa REST endpointima, njemu nije neophodno da zna kako taj server tačno radi, već sve što klijent treba da zna je da preko tih endpointova on može da komunicira sa serverom. U tom slučaju, endpointovi predstavljaju API.

4. Dati verbalni predlog strukture RESTful API-a za softver za rezervaciju avio karata. Sistem treba da podrži pretragu letova, proveru slobodnih mesta i rezervaciju mesta na letu.

| Endpoint           | Metoda | Opis                                                                                                                                                                                                           |
|--------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/api/flight/`     | GET    | Vraća sve letove. Moguće je filtriranje letova koristeći query parametara `start_city`, `finish_city` i `date`. Pružanje bilo koje kombinacije ova 3 parametara filtrira letove koji bivaju vraćeni korisniku. |
| `/api/flight/<id>` | GET    | Vraća let čiji je ID *id*.                                                                                                                                                                                      |
| `/api/flight/<id>` | POST   | Rezerviše let čiji je ID *id* ako ima slobodnih mesta, u suprotnom vraća grešku. Očekuje `body` JSON oblika koji sadrži informacije o osobi koja rezerviše let; konkretan oblik JSON-a zavisi od toga kako izgleda model korisnika.                                             |

5. Navesti barem 2 načina za obezbeđivanje responzivnosti veb stranice u CSS-u.

    1. Korišćenjem media query-ja da bismo primenili različit CSS na različitim veličinama ekrana i tako prilagodili sadržaj sajta za pregled na drugim uređajima.
    2. Korišćenjem responzivnih jedinica mere koje zavise od veličine ekrana, poput `vw`, `vh`, `em`, `rem`, `%`.

6. Navesti barem 3 načina za pozicioniranje veb stranice u pretrazi pretraživača pomoću HTML-a (SEO)

    1. Minifikacija sadržaja i smanjivanje broja zahteva radi bržeg učitavanja veb sajta.
    2. Strukturiranje dokumenta tako da bude semantičan.
    3. Pravilan odabir ključnih reči.
    4. Sklanjanje slomljenih linkova.
    5. Optimizacija za pristup preko mobilnih uređaja.

# Kod

Skidanje koda sa repozitorijuma:

    git clone https://github.com/OmegaXelix/Gang_of_Four_Project.git
    cd Gang_of_Four_Project

Repozitorijum sadrži podfoldere `backendBonus` i `prijavaTimova`; oba sadrže po jedan `README.md` sa više informacija o njima.