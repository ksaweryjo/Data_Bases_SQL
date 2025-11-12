CREATE TABLE IF NOT EXISTS Pracownicy (
    PracownikID INT PRIMARY KEY AUTO_INCREMENT,
    Imie VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Nazwisko VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Stanowisko VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    DataZatrudnienia DATE,
    Telefon VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Email VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Wynagrodzenie DECIMAL(10, 2)
)
  ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS RodzajeWycieczek (
    RodzajID INT PRIMARY KEY AUTO_INCREMENT,
    Nazwa VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Opis TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
)
  ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS KierunkiWycieczek (
    KierunekID INT PRIMARY KEY AUTO_INCREMENT,
    Lokalizacja VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Opis TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
)
  ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS Wycieczki (
    WycieczkaID INT PRIMARY KEY AUTO_INCREMENT,
    RodzajID INT NOT NULL,
    KierunekID INT NOT NULL,
    Cena DECIMAL(10, 2),
    Koszt DECIMAL(10, 2),
    FOREIGN KEY (RodzajID) REFERENCES RodzajeWycieczek(RodzajID),
    FOREIGN KEY (KierunekID) REFERENCES KierunkiWycieczek(KierunekID)
)
  ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS Klienci (
    KlientID INT PRIMARY KEY AUTO_INCREMENT,
    Imie VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Nazwisko VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Telefon VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Email VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Ulica VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Miasto VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    KontaktAlarmowyImie VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    KontaktAlarmowyTelefon VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    KontaktAlarmowyEmail VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
)
  ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS UdzialyWyjazdow (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    WycieczkaID INT NOT NULL,
    KlientID INT NOT NULL,
    FOREIGN KEY (WycieczkaID) REFERENCES Wycieczki(WycieczkaID),
    FOREIGN KEY (KlientID) REFERENCES Klienci(KlientID)
)
  ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS ZrealizowaneWyjazdy (
    WyjazdID INT PRIMARY KEY AUTO_INCREMENT,
    WycieczkaID INT NOT NULL,
    DataWyjazdu DATE,
    DataPowrotu DATE,
    PracownikID INT,
    FOREIGN KEY (WycieczkaID) REFERENCES Wycieczki(WycieczkaID),
    FOREIGN KEY (PracownikID) REFERENCES Pracownicy(PracownikID)
)
  ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS WyplatyPracownikow (
    WyplataID INT PRIMARY KEY AUTO_INCREMENT,
    PracownikID INT NOT NULL,
    Kwota DECIMAL(10, 2),
    DataWyplaty DATE,
    FOREIGN KEY (PracownikID) REFERENCES Pracownicy(PracownikID)
)
  ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;