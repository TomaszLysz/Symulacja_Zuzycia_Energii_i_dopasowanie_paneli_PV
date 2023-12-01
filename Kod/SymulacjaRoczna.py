# Wczytanie bibliotek
import importlib.util
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_library(library_name):
    spec = importlib.util.find_spec(library_name)
    if spec is None:
        install('nazwa_biblioteki')

# Sprawdzenie, czy konkretna biblioteka jest zainstalowana i jej zainstalowanie (potrzebne do udostępnienia aplikacji przeglądarkowej)
check_library('matplotlib.pyplot')

import pandas as pd
import numpy as np
import SymulacjaDzienna
import matplotlib.pyplot as plt
    


# Zdefiniowanie funkcji symulującej zużycie w danym roku oraz znajdującej najlepsze skierowanie paneli aby cena była najmniejsza a wyprodukowana energia największa
# Funkcja przyjmuje argumenty:
# Rok - rok dla którego ma zostać wykonana symulacja
# printy - zmienna mówiąca jak wiele danych należy wypisać 
# Kolumny_Produkcji - lista zawierająca nazwy wszystkich skierowań
# Prawdopodobienstwa(...) - ramki danych zawierająca pradopodobieństwo użycia danego urządzenia w danej godzinie dla każdej z pór roku
# Produkcja_Ceny - ramka danych zawierająca cenę oraz wyprodukowaną energię przez dane skierowanie dla danego dnia
# Zuzycie - ramka danych zawierająca dane dotyczące zużycia energii przez dane urządzenie
# Streamlit - zmienna dzięki której funkcja wie w jaki sposób zdefiniować wyniki (czy dostosować do terminalu czy do apliakcji przeglądarkowej)
def Funkcja_roczna(Rok, printy, Kolumny_Produkcji, PrawdopodobienstwaWiosna, PrawdopodobienstwaLato, PrawdopodobienstwaJesien, PrawdopodobienstwaZima, Produkcja_Ceny, Zuzycie, Streamlit):
    # Stworzenie zmiennej która zawiera wszystkie dni w podanym roku
    Dni = pd.date_range(Rok + '-01-01', Rok + '-12-31', freq='d')
    # Stworzenie ramek danych do których będą zapisywane wyniki symulacji dla każdego dnia
    RamkaEnergii = pd.DataFrame(columns = ['Data', 'Cena'] + Kolumny_Produkcji)
    RamkaCeny = pd.DataFrame(columns = ['Data', 'Cena'] + Kolumny_Produkcji)
    # Przypisanie do zmiennej prawdopodobieństw dla zimy ponieważ rok zaczyna się w zimie
    Prawdopodobienstwa = PrawdopodobienstwaZima
    # Stworzenie pustej listy która będzie zawiera zużycie dla każdego z dni
    ZuzycieDnia = []
    # Stworzenie pętli po każdym z dni dla dostowsowania zmiennych, wywołania funkcji symulacji dziennej dla każdego z dni oraz wpisania ich do odpowiednich ramek danych
    for iDni in Dni:
        # Dostosowanie danych do użycia do symulacji dziennej
        iDzien = str(pd.to_datetime(iDni).day).zfill(2)
        iMiesiac = str(pd.to_datetime(iDni).month).zfill(2)
        iRok = str(pd.to_datetime(iDni).year)
        # Zmiana pory roku dla prawdopodobieństw dla pierwszego dnia marca, czerwca, września oraz grudnia
        if iDzien == '01':
            if iMiesiac == '03':
                Prawdopodobienstwa = PrawdopodobienstwaWiosna
            elif iMiesiac == '06':
                Prawdopodobienstwa = PrawdopodobienstwaLato
            elif iMiesiac == '09':
                Prawdopodobienstwa = PrawdopodobienstwaJesien
            elif iMiesiac == '12':
                Prawdopodobienstwa = PrawdopodobienstwaZima
            else:
                pass
        else: 
            pass
        # Wywołanie funkcji symulacji dziennej oraz przypisanie wyników do odpowiednich zmiennych i ramek danych
        IloscOstatecznieZuzytejEnergii, CenaEnergiiZPanelami, CenaDnia, ZuzycieZDnia = SymulacjaDzienna.Funkcja_Dzienna(iRok, iMiesiac, iDzien, Prawdopodobienstwa, False, Produkcja_Ceny, Zuzycie, Kolumny_Produkcji, False)
        TempRamkaEnergii = pd.DataFrame([[iDni.date(), CenaDnia] + IloscOstatecznieZuzytejEnergii], columns = ['Data', 'Cena'] + Kolumny_Produkcji)
        RamkaEnergii = pd.concat([RamkaEnergii, TempRamkaEnergii], ignore_index = True)
        TempRamkaCeny = pd.DataFrame([[iDni.date(), CenaDnia] + CenaEnergiiZPanelami], columns = ['Data', 'Cena'] + Kolumny_Produkcji)
        RamkaCeny = pd.concat([RamkaCeny, TempRamkaCeny], ignore_index = True)
        ZuzycieDnia.append(ZuzycieZDnia)
    # Stworzenie listy zawierającej sumę zużytej energii z sieci w całym roku dla każdego skierowania
    IloscOstatecznieZuzytejEnergiiWRoku = []
    for iSkierowanie in Kolumny_Produkcji:
        IloscOstatecznieZuzytejEnergiiWRoku.append(sum(RamkaEnergii.loc[:, iSkierowanie]))
    # Stworzenie listy zawierającej najlepsze skierowania ze względu na najmniejsze zużycie energii
    SkierowaniaNaNajmniejZuzytejEnergii = []
    for index, value in enumerate(IloscOstatecznieZuzytejEnergiiWRoku):
        if value == min(IloscOstatecznieZuzytejEnergiiWRoku):
            SkierowaniaNaNajmniejZuzytejEnergii.append(Kolumny_Produkcji[index])

    # Stworzenie listy zawierającej sumę ceny za energię z sieci dla całego roku na każde skierowanie paneli PV
    CenaEnergiiZPanelamiWRoku = []
    for iSkierowanie in Kolumny_Produkcji:
        CenaEnergiiZPanelamiWRoku.append(sum(RamkaCeny.loc[:, iSkierowanie]))
    # Stworzenie listy zwierającej najlepsze skierowania ze względu na cenę zakupionej energii
    SkierowaniaNaNajmniejPieniedzy = []
    for index, value in enumerate(CenaEnergiiZPanelamiWRoku):
        if value == min(CenaEnergiiZPanelamiWRoku):
            SkierowaniaNaNajmniejPieniedzy.append(Kolumny_Produkcji[index])

    # Stworzenie listy zawierającej najlepsze skierowania ze względu na powyższe listy (część wspólna)
    WspolneSkierowania = list(set(SkierowaniaNaNajmniejZuzytejEnergii) & set(SkierowaniaNaNajmniejPieniedzy))
    # Stworzenie zmiennej zawierającej cenę za cały rok nieużywania paneli PV
    CenaRoku = sum(RamkaCeny.loc[:, 'Cena'])

    # Warunek sprawdzający w jaki sposób wypisać wyniki
    if printy == True:
        # Przygotowanie danych do wykresu
        plt.plot(Dni.strftime('%Y-%m-%d'), ZuzycieDnia)
        plt.xlabel('Dzień')
        plt.ylabel('Zużycie w danym dniu')
        plt.title('Wykres zużycia w trakcie całego roku')
        etykiety_dni = [Rok + '-01-01', Rok + '-02-01', Rok + '-03-01', Rok + '-04-01', Rok + '-05-01', Rok + '-06-01', Rok + '-07-01', Rok + '-08-01', Rok + '-09-01', Rok + '-10-01', Rok + '-11-01', Rok + '-12-01']
        plt.xticks(etykiety_dni, rotation=45)
        plt.tight_layout()
        # Warunek sprawdzający czy wynik ma być wypisany w terminalu czy w aplikacji przeglądarkowej
        if Streamlit == True:
            # Stworzenie zmiennej zawierającej wynik
            Rezultat = (
                f'**Najlepsze skierowania ({len(SkierowaniaNaNajmniejZuzytejEnergii)}) paneli ze wzgledu na najmniej energii pobranej z sieci:** \n\n {SkierowaniaNaNajmniejZuzytejEnergii}\n\n'
                f'**Najlepsze skierowania ({len(SkierowaniaNaNajmniejPieniedzy)}) paneli ze wzgledu na najmniejsza cene energii pobranej z sieci:** \n\n {SkierowaniaNaNajmniejPieniedzy}\n\n'
                        )
            if len(WspolneSkierowania) != 0:
                Rezultat = Rezultat + f'**Najlepsze skierowania ({len(WspolneSkierowania)}) ogolnie:** \n\n {WspolneSkierowania}\n\n'
            Rezultat = Rezultat + (
                f'**Cena za energie tego roku (bez paneli) wynosi: {round(CenaRoku,2)}  zl.**\n\n'
                f'**Dzieki uzyciu najlepszego skierowania zaoszczedzimy: {round(CenaRoku - min(CenaEnergiiZPanelamiWRoku),2)} zl.**\n'
                                    )
            # Zwrócenie z funkcji wykresu oraz zmiennej z wynikiem
            return(plt, Rezultat)
        else:
            # Wypisanie zmiennych w terminalu oraz jeśli to możliwe wykresu
            print('Najlepsze skierowania (', len(SkierowaniaNaNajmniejZuzytejEnergii), ') paneli ze wzgledu na najmniej energii pobranej z sieci: ', SkierowaniaNaNajmniejZuzytejEnergii)
            print('Najlepsze skierowania (',  len(SkierowaniaNaNajmniejPieniedzy) , ') paneli ze wzgledu na najmniejsza cene energii pobranej z sieci: ', SkierowaniaNaNajmniejPieniedzy)
            if len(WspolneSkierowania) != 0:
                print('Najlepsze skierowania (', len(WspolneSkierowania), ') ogolnie: ', WspolneSkierowania)
            print('Cena za energie tego roku (bez paneli) wynosi: ', round(CenaRoku,2), ' zl.')
            print('Dzieki uzyciu najlepszego skierowania zaoszczedzimy: ', round(CenaRoku - min(CenaEnergiiZPanelamiWRoku),2),' zl.')
            plt.show()
    else:
        # Wypisanie krótkich wyników
        if len(WspolneSkierowania) != 0:
            print('Najlepsze skierowania (', len(WspolneSkierowania), ') ogolnie: ', WspolneSkierowania)
        else:
            print('Najlepsze skierowania (', len(SkierowaniaNaNajmniejZuzytejEnergii), ') paneli ze wzgledu na najmniej energii pobranej z sieci: ', SkierowaniaNaNajmniejZuzytejEnergii)
            print('Najlepsze skierowania (',  len(SkierowaniaNaNajmniejPieniedzy) , ') paneli ze wzgledu na najmniejsza cene energii pobranej z sieci: ', SkierowaniaNaNajmniejPieniedzy)
        print('Cena za energie tego roku (bez paneli) wynosi: ', round(CenaRoku,2), ' zl.')
        print('Dzieki uzyciu najlepszego skierowania zaoszczedzimy: ', round(CenaRoku - min(CenaEnergiiZPanelamiWRoku),2),' zl.')

    
    












