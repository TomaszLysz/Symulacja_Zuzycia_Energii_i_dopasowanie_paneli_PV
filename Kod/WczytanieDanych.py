# Załadowanie bibliotek
import os
import pandas as pd


# Zdefiniowanie funkcji wczytującej pliki z cenami rynkowymi energii elektrycznej
# Funkcja przyjmuje tylko jeden argument który jest ścieżką do głównego folderu z plikami
def WczytanieCenyEnergii(Sciezka):
    # Uzupełnienie ścieżki o odpowiedni folder
    Sciezka = Sciezka + r'/Ceny rynkowe'
    # Pobranie listy plików w folderze
    ListaPlikow = os.listdir(Sciezka)
    # Pętla po każdym z plików pobierająca go i doklejająca do ramki danych
    for i in ListaPlikow:
        Plik = Sciezka + '\\' + i
        Dane = pd.read_csv(Plik, sep = ';', encoding = 'latin-1')
        Dane.columns = ['Data', 'Godzina', 'Cena']
        if i == ListaPlikow[0]:
            WszystkieCeny = Dane
        else:
            WszystkieCeny = pd.concat([WszystkieCeny, Dane])
    # Usunięcie części danych ponieważ są one do końca 2022 roku a inne dane są do końca 2020
    CenaPradu = WszystkieCeny.iloc[:26304]
    # Oczyszczenie danych
    CenaPradu.loc[:, 'Cena'] = CenaPradu['Cena'].str.replace(',','.').replace(' ','').str.replace('\xa0','').astype(float)
    # Dodanie pierwszego wiersza który nie znajduję się w danych
    PierwszyWiersz = pd.DataFrame({'Data': [20171231], 'Godzina': [24], 'Cena': [210.00]})
    CenaPradu = pd.concat([PierwszyWiersz, CenaPradu], ignore_index= True)
    # Usunięcie ostatniego wiersza który jest już na następny rok
    CenaPradu = CenaPradu.drop(CenaPradu.index[-1])
    # Operacje na danych aby stworzyć odpowiednią datę
    CenaPradu['Data'] = pd.to_datetime(CenaPradu['Data'], format='%Y%m%d')
    CenaPradu.loc[CenaPradu['Godzina'] == 24, 'Godzina'] = 0
    CenaPradu.loc[CenaPradu['Godzina'] == '24', 'Godzina'] = 0
    CenaPradu.loc[CenaPradu['Godzina'] == 0, 'Data'] = pd.to_datetime(CenaPradu.loc[CenaPradu['Godzina'] == 0, 'Data']) + pd.DateOffset(days=1)
    CenaPradu['Data'] = CenaPradu['Data'].astype(str)
    CenaPradu['Godzina'] = CenaPradu['Godzina'].astype(str).str.replace('2A','2')
    CenaPradu['Data'] = CenaPradu['Data'] + ' ' + CenaPradu['Godzina']
    CenaPradu['Data'] = pd.to_datetime(CenaPradu['Data'], format='%Y-%m-%d %H')
    # Dostosowanie odpowiedniej jednostki ceny
    CenaPradu['Cena'] = CenaPradu['Cena']/1000
    # Zwrócenie z funkcji pojedynczej ramki danych
    return(CenaPradu)


# Funkcja zczytująca dane dotyczące produkcji energii elektrycznej przez panele o danym skierowaniu
# Funkcja przyjmuję jeden argument którym jest ścieżka do ogólnego folderu z plikami
def WczytanieProdukcjiEnergiiPrzezPanele(Sciezka):
    # Uzupełnienie ścieżki o odpowiedni folder
    Sciezka = Sciezka + r'/Hourly radiaton data'
    # Pobranie listy plików w folderze
    ListaPlikow = os.listdir(Sciezka)
    # Pętla po każdym z plików pobierająca go i doklejająca do ramki danych
    for i in ListaPlikow:
        Plik = Sciezka+'/'+i
        Dane = pd.read_csv(Plik, sep = ',', skiprows = 10, nrows = 26304).drop(['G(i)', 'H_sun', 'T2m', 'WS10m', 'Int'], axis = 1)
        NazwaPliku = i.replace('Timeseries_49.915_21.866_SA2_1kWp_crystSi_14_','').replace('_2018_2020.csv','').replace('_', ' ')
        Dane.columns = ['Data', NazwaPliku]
        if i == ListaPlikow[0]:
            WyprodukowanaEnergia = Dane
        else:
            WyprodukowanaEnergia[NazwaPliku] = Dane[NazwaPliku]
    # Zmiana formatu na datę w kolumnie data
    WyprodukowanaEnergia['Data'] = pd.to_datetime(WyprodukowanaEnergia['Data'], format='%Y%m%d:%H%M')
    # Zwrócenie z funkcji pojedynczej ramki danych
    return(WyprodukowanaEnergia)

# Zdefiniowanie funkcji wczytującej pliki z zużyciem i prawdopodobieństwem użycia danych urządzeń
# Funkcja przyjmuje trzy argumenty: Scieżka do ogólnego folderu z plikami, Tryb czyli czy symulacja jest roczna czy dzienna oraz Model czyli który model zużycia energii jest wczytywany
def WczytaniePrawdopodobienstwaUrzadzen(Sciezka, Tryb, Model):
    # Uzupełnienie ścieżki o odpowiedni folder
    Sciezka = Sciezka + r'/Urzadzenia'
    # Sprawdzenie Trybu
    if Tryb == True:
        # Sprawdzenie modelu a następnie uzupełnienie ścieżki o odpowiednią nazwę pliku
        if Model == '1':
            Sciezka = Sciezka + r'/Urzadzenia1.csv'
        elif Model == '2':
            Sciezka = Sciezka + r'/Urzadzenia2.csv'
        elif Model == '3':
            Sciezka = Sciezka + r'/Urzadzenia3.csv'
        # Wczytanie plików    
        Prawdopodobienstwa = pd.read_csv(Sciezka, sep = ',', skiprows = 2)
        Zuzycie = pd.read_csv(Sciezka, sep = ',', nrows = 1)
        # Zwrócenie z funkcji dwóch ramek danych, z prawdopodobieństwem użycia oraz zużyciem energii danego urządzenia
        return(Prawdopodobienstwa, Zuzycie)
    # Sprawdzenie Trybu
    elif Tryb == False:
        # Sprawdzenie modelu a następnie uzupełnienie ścieżki o odpowiednią nazwę pliku
        if Model == '1':
            ModelZuzyc = r'/Urzadzenia1'
        elif Model == '2':
            ModelZuzyc = r'/Urzadzenia2'
        elif Model == '3':
            ModelZuzyc = r'/Urzadzenia3'
        ULato = ModelZuzyc + r' — Lato.csv'
        UWiosJes = ModelZuzyc+  r' — Wiosna i Jesien.csv'
        UZima = ModelZuzyc + r' — Zima.csv'
        # Wczytanie plików  
        PrawdopodobienstwaLato = pd.read_csv(Sciezka + ULato, sep = ',', skiprows = 2)
        PrawdopodobienstwaJesien = pd.read_csv(Sciezka + UWiosJes, sep = ',', skiprows = 2)
        PrawdopodobienstwaZima = pd.read_csv(Sciezka + UZima, sep = ',', skiprows = 2)
        PrawdopodobienstwaWiosna = pd.read_csv(Sciezka + UWiosJes, sep = ',', skiprows = 2)
        Zuzycie = pd.read_csv(Sciezka + ULato, sep = ',', nrows = 1)
         # Zwrócenie z funkcji dwóch ramek danych, z prawdopodobieństwem użycia oraz zużyciem energii danego urządzenia
        return(PrawdopodobienstwaWiosna, PrawdopodobienstwaLato, PrawdopodobienstwaJesien, PrawdopodobienstwaZima, Zuzycie)


# Funkcja łącząca ramki danych z ceną prądu oraz wyprodukowaną energią
def OperacjeNaDanych(CenaPradu, WyprodukowanaEnergia):
    # Polaczenie ramek danych
    Produkcja_Ceny = pd.concat([CenaPradu['Cena'], WyprodukowanaEnergia], axis = 1)
    # Wczytanie nazw skierowań do listy
    Kolumny_Produkcji = WyprodukowanaEnergia.columns[1:].tolist()
    # Dodanie dwóch kolumn do ramki danych
    Produkcja_Ceny = Produkcja_Ceny[['Data', 'Cena'] + Kolumny_Produkcji]
    # Zwrócenie z funkcji połączonej ramki danych oraz listy z nazwami skierowań
    return(Produkcja_Ceny, Kolumny_Produkcji)





