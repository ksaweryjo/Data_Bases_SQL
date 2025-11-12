import mysql.connector
import random
from datetime import datetime, timedelta
from faker import Faker
import unidecode  # do usunięcia polskich znaków z imion/nazwisk

# Konfiguracja Faker z polską lokalizacją
fake = Faker("pl_PL")

# Połączenie z bazą danych
conn = mysql.connector.connect(
    host="giniewicz.it",
    user="team25",
    password="te@mzazs",
    database="team25",
    charset='utf8mb4'
)
cursor = conn.cursor()

# Zbiór wszystkich wykorzystanych e-maili (dla unikalności)
zajete_maile = set()


def generuj_email(imie, nazwisko, domena="example.com"):
    """
    Generuje unikalny adres e-mail w formacie
      imie.nazwisko[@domena],
    bez polskich znaków i z ewentualnym numerkiem,
    jeśli już istnieje w zbiorze zajete_maile.
    """
    imie_ascii = unidecode.unidecode(imie).lower()
    nazwisko_ascii = unidecode.unidecode(nazwisko).lower()

    base_email = f"{imie_ascii}.{nazwisko_ascii}"
    base_email = base_email.replace(" ", "")  # usuń spacje, jeśli jakieś wystąpiły

    candidate = f"{base_email}@{domena}"
    counter = 1

    while candidate in zajete_maile:
        candidate = f"{base_email}{counter}@{domena}"
        counter += 1

    zajete_maile.add(candidate)
    return candidate


def generuj_telefon():
    numer = random.randint(500000000, 899999999)
    return f"+48{numer}"


# Domena firmowa dla pracowników
DOMENA_FIRMOWA = "firma.com"

# Dla klientów - realistyczne domeny
DOMENY_KLIENTOW = ["gmail.com", "o2.pl", "interia.pl", "wp.pl", "onet.pl"]

#
# 1. Dodawanie pracowników
#
pracownicy = []
for _ in range(5):
    imie = fake.first_name()
    nazwisko = fake.last_name()

    email = generuj_email(imie, nazwisko, domena=DOMENA_FIRMOWA)

    stanowisko = random.choice(["Przewodnik", "Kierowca", "Koordynator", "Obsługa klienta"])
    wynagrodzenie = round(random.uniform(3600, 7000), 2)

    # Data zatrudnienia z ostatnich 2 lat
    days_back = random.randint(0, 730)
    data_zatrudnienia = (datetime.now() - timedelta(days=days_back)).date()

    telefon = generuj_telefon()

    cursor.execute("""
        INSERT INTO Pracownicy 
        (Imie, Nazwisko, Stanowisko, DataZatrudnienia, Telefon, Email, Wynagrodzenie)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (imie, nazwisko, stanowisko, data_zatrudnienia, telefon, email, wynagrodzenie))

    pracownicy.append((imie, nazwisko, wynagrodzenie))

conn.commit()

#
# 2. Dodawanie RODZAJÓW WYIECZEK
#
rodzaje_wycieczek_lista = ["Survival", "Wieczór kawalerski", "Koncert", "Zwiedzanie", "Ekstremalne"]
opisy_rodzajow_lista = [
    "Wyprawy w nieznane z elementami survivalu",
    "Inscenizowane porwania i przygody na wieczór kawalerski",
    "Koncerty dla fanów niszowej muzyki",
    "Eksploracja zabytków i miejsc kulturowych",
    "Przygody dla miłośników adrenaliny"
]
for nazwa, opis in zip(rodzaje_wycieczek_lista, opisy_rodzajow_lista):
    cursor.execute(
        "INSERT INTO RodzajeWycieczek (Nazwa, Opis) VALUES (%s, %s)",
        (nazwa, opis)
    )
conn.commit()

#
# 3. Dodawanie KIERUNKÓW
#
miasta_lista = ["Warszawa", "Kraków", "Gdańsk", "Poznań", "Wrocław"]
opisy_miast = {
    "Warszawa": "Stolica Polski z bogatą historią i nowoczesnym obliczem.",
    "Kraków": "Królewskie miasto pełne zabytków i kultury.",
    "Gdańsk": "Portowe miasto nad Bałtykiem, znane z długiej historii.",
    "Poznań": "Miasto koziołków i centrum biznesowe Wielkopolski.",
    "Wrocław": "Miasto mostów i krasnali, z bogatą historią i kulturą."
}
for miasto in miasta_lista:
    opis_miasta = opisy_miast.get(miasto, "")
    cursor.execute(
        "INSERT INTO KierunkiWycieczek (Lokalizacja, Opis) VALUES (%s, %s)",
        (miasto, opis_miasta)
    )
conn.commit()

#
# 4. Dodawanie WYIECZEK (ofert) - 10 sztuk
#
wycieczki = []
for _ in range(10):
    rodzaj_id = random.randint(1, len(rodzaje_wycieczek_lista))  # 1..5
    kierunek_id = random.randint(1, len(miasta_lista))  # 1..5
    cena = random.choice([1000, 1500, 2000, 3000, 5000])
    koszt = round(cena * random.uniform(0.6, 0.9), 2)  # mniej niż cena

    cursor.execute("""
        INSERT INTO Wycieczki (RodzajID, KierunekID, Cena, Koszt)
        VALUES (%s, %s, %s, %s)
    """, (rodzaj_id, kierunek_id, cena, koszt))

    wycieczki.append((rodzaj_id, kierunek_id, cena, koszt))

conn.commit()

#
# 5. Dodawanie KLIENTÓW (30 osób)
#
klienci = []
for _ in range(30):
    imie = fake.first_name()
    nazwisko = fake.last_name()

    domena_klienta = random.choice(DOMENY_KLIENTOW)
    email_klienta = generuj_email(imie, nazwisko, domena=domena_klienta)
    telefon = generuj_telefon()
    ulica = fake.street_address()
    miasto = fake.city()
    kontakt_imie = fake.first_name()
    kontakt_nazwisko = fake.last_name()
    domena_kontakt = random.choice(DOMENY_KLIENTOW)
    kontakt_email = generuj_email(kontakt_imie, kontakt_nazwisko, domena=domena_kontakt)
    kontakt_telefon = generuj_telefon()

    cursor.execute("""
        INSERT INTO Klienci 
        (Imie, Nazwisko, Telefon, Email, 
         Ulica, Miasto, 
         KontaktAlarmowyImie, KontaktAlarmowyTelefon, KontaktAlarmowyEmail)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (imie, nazwisko, telefon, email_klienta,
          ulica, miasto,
          kontakt_imie, kontakt_telefon, kontakt_email))

    klienci.append((imie, nazwisko, email_klienta))

conn.commit()

#
# 6. Dodawanie ZREALIZOWANYCH WYJAZDÓW (10 - każdy wyjazd inny)
#
zrealizowane_wyjazdy = []
# Uwzględniamy każde id ale losowo
wycieczka_ids = list(range(1, 11))  # 1..10
random.shuffle(wycieczka_ids)  # Losowa kolejność

for wycieczka_id in wycieczka_ids:
    pracownik_id = random.randint(1, 5)

    days_back_start = random.randint(0, 365)
    data_wyjazdu = (datetime.now() - timedelta(days=days_back_start)).date()
    days_duration = random.randint(3, 10)
    data_powrotu = data_wyjazdu + timedelta(days=days_duration)

    cursor.execute("""
        INSERT INTO ZrealizowaneWyjazdy 
        (WycieczkaID, DataWyjazdu, DataPowrotu, PracownikID)
        VALUES (%s, %s, %s, %s)
    """, (wycieczka_id, data_wyjazdu, data_powrotu, pracownik_id))

    zrealizowane_wyjazdy.append(cursor.lastrowid)
conn.commit()

#
# 7. Dodawanie UDZIAŁÓW WYJAZDÓW (30 losowych - zależne od zrealizowanych wyjazdów)
#
for _ in range(30):
    zrealizowany_wyjazd_id = random.choice(zrealizowane_wyjazdy)  # Powiązanie z realizowanymi wyjazdami
    klient_id = random.randint(1, 30)  # 30 klientów

    cursor.execute("""
        INSERT INTO UdzialyWyjazdow (WycieczkaID, KlientID)
        SELECT WycieczkaID, %s FROM ZrealizowaneWyjazdy WHERE WyjazdID = %s
    """, (klient_id, zrealizowany_wyjazd_id))

conn.commit()

#
# 8. Dodawanie WYPŁAT (12 wypłat dla każdego pracownika)
#
now = datetime.now()
for pracownik_id in range(1, 6):
    # Pobierz wynagrodzenie z tabeli Pracownicy
    cursor.execute("SELECT Wynagrodzenie FROM Pracownicy WHERE PracownikID = %s", (pracownik_id,))
    row = cursor.fetchone()
    if row:
        wynagrodzenie_miesieczne = row[0]
    else:
        wynagrodzenie_miesieczne = 4000  # fallback

    # Generujemy 12 wypłat za ostatnie 12 miesięcy:
    for i in range(12):
        rok = now.year
        miesiac = now.month - i
        while miesiac <= 0:
            miesiac += 12
            rok -= 1

        dzien = random.randint(1, 10)  # Losowy dzień 1..10
        data_wyplaty = datetime(rok, miesiac, dzien).date()

        cursor.execute("""
            INSERT INTO WyplatyPracownikow (PracownikID, Kwota, DataWyplaty)
            VALUES (%s, %s, %s)
        """, (pracownik_id, wynagrodzenie_miesieczne, data_wyplaty))

conn.commit()

cursor.close()
conn.close()

print("Skrypt zakończył działanie. ")