# Wczytanie plików z funkcjami
import WczytanieDanych
import SymulacjaDzienna
import SymulacjaRoczna


# Zdefiniowanie ścieżki do folderu z plikami
Sciezka = r'E:\STUDIA\Inzynierka - Python\Pliki'

# Zdefiniowanie funkcji uruchamiającej cały program
# Funckja przyjmuję argumenty:
# Sciezka - ścieżka do folderu z plikami
# Rok, Miesiac, Dzien - zdefinowane parametry określające dany dzień w symulacji (lub rok)
# Tryb - zmienna mówiąca czy symulacja ma być dzienna czy roczna
# Streamlit - zmienna mówiąca czy wynik symulacji będzie wyświetlany w terminalu czy w aplikacji przeglądarkowej
# Model - zmienna mówiąca jaki model zużycia energii jest brany pod uwagę w symulacji
def Funkcja_main(Sciezka, Rok, Miesiac, Dzien, Tryb, Streamlit, Model):
    # Uzupełnienie zmiennych do formatu przyjmowanego w funkcji
    Miesiac = Miesiac.zfill(2)
    Dzien = Dzien.zfill(2)
    if Tryb == 'Dzienna':
        Tryb = True
    else:
        Tryb = False
    printy = True
    # Zdefiniowanie funkcji wczytującej wszystkie dane potrzebne dla danej symulacji
    def WczytanieWszystkichDanych(Sciezka, Tryb, Model):
        CenaPradu = WczytanieDanych.WczytanieCenyEnergii(Sciezka)
        WyprodukowanaEnergia = WczytanieDanych.WczytanieProdukcjiEnergiiPrzezPanele(Sciezka)
        Produkcja_Ceny, Kolumny_Produkcji = WczytanieDanych.OperacjeNaDanych(CenaPradu, WyprodukowanaEnergia) 
        if Tryb == True:
            Prawdopodobienstwa, Zuzycie = WczytanieDanych.WczytaniePrawdopodobienstwaUrzadzen(Sciezka, Tryb, Model)
            return(CenaPradu, WyprodukowanaEnergia, Prawdopodobienstwa, Zuzycie, Produkcja_Ceny, Kolumny_Produkcji)
        else:
            PrawdopodobienstwaWiosna, PrawdopodobienstwaLato, PrawdopodobienstwaJesien, PrawdopodobienstwaZima, Zuzycie = WczytanieDanych.WczytaniePrawdopodobienstwaUrzadzen(Sciezka, Tryb, Model)
            return(CenaPradu, WyprodukowanaEnergia, PrawdopodobienstwaWiosna, PrawdopodobienstwaLato, PrawdopodobienstwaJesien, PrawdopodobienstwaZima, Zuzycie, Produkcja_Ceny, Kolumny_Produkcji)
        
    # Wywołanie symulacji dziennej
    if Tryb == True:
        CenaPradu, WyprodukowanaEnergia, Prawdopodobienstwa, Zuzycie, Produkcja_Ceny, Kolumny_Produkcji = WczytanieWszystkichDanych(Sciezka, Tryb, Model)
        y ,x = SymulacjaDzienna.Funkcja_Dzienna(Rok, Miesiac, Dzien, Prawdopodobienstwa, printy, Produkcja_Ceny, Zuzycie, Kolumny_Produkcji, Streamlit)


    # Wywołanie symulacji rocznej
    else:
        CenaPradu, WyprodukowanaEnergia, PrawdopodobienstwaWiosna, PrawdopodobienstwaLato, PrawdopodobienstwaJesien, PrawdopodobienstwaZima, Zuzycie, Produkcja_Ceny, Kolumny_Produkcji = WczytanieWszystkichDanych(Sciezka, Tryb, Model)
        y, x = SymulacjaRoczna.Funkcja_roczna(Rok, printy, Kolumny_Produkcji, PrawdopodobienstwaWiosna, PrawdopodobienstwaLato, PrawdopodobienstwaJesien, PrawdopodobienstwaZima, Produkcja_Ceny, Zuzycie, Streamlit)

    # Zwrócenie wyników symulacji                          
    return(y, x)





