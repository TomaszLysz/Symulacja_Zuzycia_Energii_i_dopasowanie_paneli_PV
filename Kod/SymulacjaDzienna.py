# Wczytanie bibliotek
import pandas as pd
import random
import numpy as np
# import matplotlib.pyplot as plt


# Zdefiniowanie funkcji symulującej zużycie w danym dniu oraz znajdującej najlepsze skierowanie paneli aby cena była najmniejsza a wyprodukowana energia największa
# Funkcja przyjmuję argumenty: 
# - Rok, Miesiac, Dzien aby pobrać dane dotyczące ceny i produkcji w danym dniu
# - Prawdopodobienstwa czyli prawdopodobieństwo użycia danego urządzenia w danej godzinie
# - printy czyli zmienna mówiąca, czy funkcja ma wypisywać swój wynik czy zwrócić wartości (druga wersja jest używana w symulacji roku)
# - Produkcja_Ceny czyli Ramka danych zawierająca cenę prądu oraz wyprodukowanie energii przez panele
# - Zuzycie czyli Ramka danych w której są informacje dotyczące zużycia prądu przez dane urządzenie
# - Kolumny_Produkcji czyli lista z nazwami wszystkich skierowań
# - Streamlit aby dostosować dane zwrotne do aplikacji przeglądarkowej
def Funkcja_Dzienna(Rok, Miesiac, Dzien, Prawdopodobienstwa, printy, Produkcja_Ceny, Zuzycie, Kolumny_Produkcji, Streamlit):
    # Znalezienie indeksu zadanego dnia w danych
    Dni = Produkcja_Ceny.loc[Produkcja_Ceny['Data'] == Rok + Miesiac + Dzien +' 00:10:00'].index[0]
    # Wczytanie danych z ceną oraz produkcją z zadanego dnia oraz operacje na nich
    DaneDnia = Produkcja_Ceny.iloc[range(Dni, Dni + 24),]
    DaneDnia.reset_index(drop = True, inplace = True)
    # Dodanie dwóch pustych kolumn
    DaneDnia.insert(2, 'Zuzycie', 0, True)
    DaneDnia.insert(3, 'Wartosc zuzytej energii', 0, True)
    # Pętla po każdym urządzeniu i każdej godzinie losująca zużycie dla każdej godziny
    for iUrzadzen in Zuzycie.columns:
        for iGodzin in range(24):
            Los = round(random.uniform(0.00, 1.00),4)
            if Los <= Prawdopodobienstwa[iUrzadzen][iGodzin]:
                DaneDnia.loc[iGodzin, 'Zuzycie'] = DaneDnia.loc[iGodzin, 'Zuzycie'] + Zuzycie.loc[0, iUrzadzen]
    # Uzupełnienie kolumny z wartością zużytej energii jako pomnożenie zużycia z ceną z danej godziny
    DaneDnia.loc[:,'Wartosc zuzytej energii']  = DaneDnia.loc[:, 'Zuzycie'] * DaneDnia.loc[:, 'Cena']          
    # Odjęcie od zużycia wyprodukowanej energii dla każdego ze skierowań (jeśli wartość jest ujemna zmienia się na 0)
    for iSkierowanie in Kolumny_Produkcji:
        for iGodzin in range(24):
            DaneDnia.loc[iGodzin, iSkierowanie] = np.maximum(0, DaneDnia.loc[iGodzin, 'Zuzycie'] - DaneDnia.loc[iGodzin, iSkierowanie])
    # Stworzenie listy z ilością zużytej energii w danym dniu dla każdego skierowania (suma po kolumnie dla każdego skierowania)
    IloscOstatecznieZuzytejEnergii = []
    for iSkierowanie in Kolumny_Produkcji:
        IloscOstatecznieZuzytejEnergii.append(sum(DaneDnia.loc[:, iSkierowanie]))
    # Znalezienie najlepszych skierowań ze względu na najmniej zużytej energii z sieci (minimum z wcześniej stworzonej listy)
    SkierowaniaNaNajmniejZuzytejEnergii = []
    for index, value in enumerate(IloscOstatecznieZuzytejEnergii):
        if value == min(IloscOstatecznieZuzytejEnergii):
            SkierowaniaNaNajmniejZuzytejEnergii.append(Kolumny_Produkcji[index])
    # Storzenie ramki danych zawierającej cenę zakupionej energii dla każdego skierowania w każdej godzinie
    DaneDniaCena = DaneDnia
    for iSkierowanie in Kolumny_Produkcji:
        for iGodzin in range(24):
            DaneDniaCena.loc[iGodzin, iSkierowanie] = DaneDnia.loc[iGodzin, 'Cena'] * DaneDnia.loc[iGodzin, iSkierowanie]
    # Stworzenie listy z ceną zakupionej energii w danym dniu dla każdego skierowania
    CenaEnergiiZPanelami = []
    for iSkierowanie in Kolumny_Produkcji:
        CenaEnergiiZPanelami.append(sum(DaneDnia.loc[:, iSkierowanie]))
    # Znalezienie najlepszych skierowań ze względu na najmniej zakupionej energii z sieci (minimum z wcześniej stworzonej listy)
    SkierowaniaNaNajmniejPieniedzy = []
    for index, value in enumerate(CenaEnergiiZPanelami):
        if value == min(CenaEnergiiZPanelami):
            SkierowaniaNaNajmniejPieniedzy.append(Kolumny_Produkcji[index])


    # Znalezienie najlepszego skierowania ze względu na wcześniej stworzone listy (część wspólna z obu list) 
    WspolneSkierowania = list(set(SkierowaniaNaNajmniejZuzytejEnergii) & set(SkierowaniaNaNajmniejPieniedzy))


    # Operacje na danych dla wykresu
    # Zsumowanie ceny energii dla każdej godziny aby zdobyć cenę energii dla całego dnia
    CenaDnia = sum(DaneDnia.loc[:, 'Wartosc zuzytej energii'])
    # Zsumowanie zużycia energii dla każdej godziny aby zdobyć zużycie dla całego dnia
    ZuzycieJednegoDnia = sum(DaneDnia.loc[:, 'Zuzycie'])
    # Stworzenie listy zawierającej zużycie dla każdej godziny
    ZuzycieDnia = DaneDnia.loc[:, 'Zuzycie']
    # Stworzenie listy z godzinami
    Czas = DaneDnia.loc[:, 'Data']
    Czas = Czas.dt.strftime('%H')
    
    # Warunek sprawdzający czy należy wypisać wyniki i stworzyć wykres
    if printy == True:
        # Szczegóły do wykresu
        # plt.plot(Czas, ZuzycieDnia)
        # plt.xlabel('Godzina')
        # plt.ylabel('Zużycie w danej godzinie')
        # plt.title('Wykres zużycia w trakcie jednego dnia')
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # Warunek sprawdzający czy wypisanie wyników ma byćw aplikacji czy terminalu
        if Streamlit == False:
            # Wypisanie wyników i wyświetlenie wykresu
            print('Najlepsze skierowania (', len(SkierowaniaNaNajmniejZuzytejEnergii), ') paneli ze wzgledu na najmniej energii pobranej z sieci: ', SkierowaniaNaNajmniejZuzytejEnergii)
            print('Najlepsze skierowania (',  len(SkierowaniaNaNajmniejPieniedzy) , ') paneli ze wzgledu na najmniejsza cene energii pobranej z sieci: ', SkierowaniaNaNajmniejPieniedzy)
            if len(WspolneSkierowania) != 0:
                print('Najlepsze skierowania (', len(WspolneSkierowania), ') ogolnie: ', WspolneSkierowania)
            print('Cena za energie tego dnia (bez paneli) wynosi: ', round(CenaDnia,2), ' zl.')
            print('Dzieki uzyciu najlepszego skierowania zaoszczedzimy: ', round(CenaDnia - min(CenaEnergiiZPanelami),2),' zl.')
            # plt.show()

        else:
            # Przypisanie do zmiennej wyników oraz zwrócenie jej wraz z wykresem
            Rezultat =  (
                    f'**Najlepsze skierowania ({len(SkierowaniaNaNajmniejZuzytejEnergii)}) paneli ze względu na najmniej energii pobranej z sieci:** \n\n{SkierowaniaNaNajmniejZuzytejEnergii}\n\n'
                    f'**Najlepsze skierowania ({len(SkierowaniaNaNajmniejPieniedzy)}) paneli ze względu na najmniejszą cenę energii pobranej z sieci:** \n\n{SkierowaniaNaNajmniejPieniedzy}\n\n'
                        )
            if len(WspolneSkierowania) != 0:
                    Rezultat = Rezultat + f'**Najlepsze skierowania ({len(WspolneSkierowania)}) ogólnie:** \n\n{WspolneSkierowania}\n\n'
            Rezultat = Rezultat + (
                    f'**Cena za energię tego dnia (bez paneli) wynosi: {round(CenaDnia, 2)} zł.**\n\n'
                    f'**Dzięki użyciu najlepszego skierowania zaoszczędzimy: {round(CenaDnia - min(CenaEnergiiZPanelami), 2)} zł.**'
            )
            plt = 'xD'
            return(plt, Rezultat)
            

    else:
        # Zwrócenie danych z funkcji
        return(IloscOstatecznieZuzytejEnergii, CenaEnergiiZPanelami, CenaDnia, ZuzycieJednegoDnia)
    


    