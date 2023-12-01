import os
import pandas as pd
import random
import numpy as np

Sciezka = r'E:\STUDIA\Inzynierka - Python\Pliki\Ceny rynkowe'
ListaPlikow = os.listdir(Sciezka)

for i in ListaPlikow:
    Plik = Sciezka+'\\'+i
    Dane = pd.read_csv(Plik, sep = ';', encoding = 'latin-1')
    Dane.columns = ['Data', 'Godzina', 'Cena']
    if i == ListaPlikow[0]:
        WszystkieCeny = Dane
    else:
        WszystkieCeny = pd.concat([WszystkieCeny, Dane])
    
CenaPradu = WszystkieCeny.iloc[:26304]

CenaPradu.loc[:, 'Cena'] = CenaPradu['Cena'].str.replace(',','.').replace(' ','').str.replace('\xa0','').astype(float)
# Dodanie pierwszej godziny bo nie ma danych
PierwszyWiersz = pd.DataFrame({
    'Data': [20171231], 'Godzina': [24], 'Cena': [210.00]
})
CenaPradu = pd.concat([PierwszyWiersz, CenaPradu], ignore_index= True)

# Usuniecie ostatniego wiersza bo to juz nastepny dzien
CenaPradu = CenaPradu.drop(CenaPradu.index[-1])

CenaPradu['Data'] = pd.to_datetime(CenaPradu['Data'], format='%Y%m%d')

CenaPradu.loc[CenaPradu['Godzina'] == 24, 'Godzina'] = 0
CenaPradu.loc[CenaPradu['Godzina'] == '24', 'Godzina'] = 0
CenaPradu.loc[CenaPradu['Godzina'] == 0, 'Data'] = pd.to_datetime(CenaPradu.loc[CenaPradu['Godzina'] == 0, 'Data']) + pd.DateOffset(days=1)

CenaPradu['Data'] = CenaPradu['Data'].astype(str)
CenaPradu['Godzina'] = CenaPradu['Godzina'].astype(str)
CenaPradu['Godzina'] = CenaPradu['Godzina'].str.replace('2A','2')

CenaPradu['Data'] = CenaPradu['Data'] + ' ' + CenaPradu['Godzina']

CenaPradu['Cena'] = CenaPradu['Cena']/1000

CenaPradu['Data'] = pd.to_datetime(CenaPradu['Data'], format='%Y-%m-%d %H')

Sciezka = r'E:\STUDIA\Inzynierka - Python\Pliki\Hourly radiaton data'
ListaPlikow = os.listdir(Sciezka)

for i in ListaPlikow:
    Plik = Sciezka+'\\'+i
    Dane = pd.read_csv(Plik, sep = ',', skiprows = 10, nrows = 26304).drop(['G(i)', 'H_sun', 'T2m', 'WS10m', 'Int'], axis = 1)
    NazwaPliku = i.replace('Timeseries_49.915_21.866_SA2_1kWp_crystSi_14_','').replace('_2018_2020.csv','').replace('_', ' ')
    Dane.columns = ['Data', NazwaPliku]
    if i == ListaPlikow[0]:
        WyprodukowanaEnergia = Dane
    else:
        WyprodukowanaEnergia[NazwaPliku] = Dane[NazwaPliku]

WyprodukowanaEnergia['Data'] = pd.to_datetime(WyprodukowanaEnergia['Data'], format='%Y%m%d:%H%M')

Sciezka = r'E:\STUDIA\Inzynierka - Python\Pliki\Urzadzenia\Urzadzenia1.csv'
Prawdopodobienstwa = pd.read_csv(Sciezka, sep = ',', skiprows = 2)
Zuzycie = pd.read_csv(Sciezka, sep = ',', nrows = 1)

Produkcja_Ceny = pd.concat([CenaPradu['Cena'], WyprodukowanaEnergia], axis = 1)
Kolumny_Produkcji = ['0deg -120deg', '0deg -150deg', '0deg -179deg',
       '0deg -30deg', '0deg -60deg', '0deg -90deg', '0deg 0deg', '0deg 120deg',
       '0deg 150deg', '0deg 30deg', '0deg 60deg', '0deg 90deg',
       '15deg -120deg', '15deg -150deg', '15deg -179deg', '15deg -30deg',
       '15deg -60deg', '15deg -90deg', '15deg 0deg', '15deg 120deg',
       '15deg 150deg', '15deg 30deg', '15deg 60deg', '15deg 90deg',
       '30deg -120deg', '30deg -150deg', '30deg -179deg', '30deg -30deg',
       '30deg -60deg', '30deg -90deg', '30deg 0deg', '30deg 120deg',
       '30deg 150deg', '30deg 30deg', '30deg 60deg', '30deg 90deg',
       '45deg -120deg', '45deg -150deg', '45deg -179deg', '45deg -30deg',
       '45deg -60deg', '45deg -90deg', '45deg 0deg', '45deg 120deg',
       '45deg 150deg', '45deg 30deg', '45deg 60deg', '45deg 90deg',
       '60deg -120deg', '60deg -150deg', '60deg -179deg', '60deg -30deg',
       '60deg -60deg', '60deg -90deg', '60deg 0deg', '60deg 120deg',
       '60deg 150deg', '60deg 30deg', '60deg 60deg', '60deg 90deg',
       '75deg -120deg', '75deg -150deg', '75deg -179deg', '75deg -30deg',
       '75deg -60deg', '75deg -90deg', '75deg 0deg', '75deg 120deg',
       '75deg 150deg', '75deg 30deg', '75deg 60deg', '75deg 90deg',
       '90deg -120deg', '90deg -150deg', '90deg -179deg', '90deg -30deg',
       '90deg -60deg', '90deg -90deg', '90deg 0deg', '90deg 120deg',
       '90deg 150deg', '90deg 30deg', '90deg 60deg', '90deg 90deg']
Produkcja_Ceny = Produkcja_Ceny[['Data', 'Cena'] + Kolumny_Produkcji]

def Funkcja_Dzienna(Rok, Miesiac, Dzien, TypPrawdopodobienstw, printy):
    Dni = Produkcja_Ceny.loc[Produkcja_Ceny['Data'] == Rok + Miesiac + Dzien +' 00:10:00'].index[0]
    DaneDnia = Produkcja_Ceny.iloc[range(Dni, Dni + 24),]
    DaneDnia.reset_index(drop = True, inplace = True)
    DaneDnia.insert(2, 'Zuzycie', 0, True)
    DaneDnia.insert(3, 'Wartosc zuzytej energii', 0, True)
    
    
    
    # Losowanie zuzycia
    for iUrzadzen in Zuzycie.columns:
        for iGodzin in range(24):
            Los = round(random.uniform(0.00, 1.00),4)
            if Los <= TypPrawdopodobienstw[iUrzadzen][iGodzin]:
                DaneDnia.loc[iGodzin, 'Zuzycie'] = DaneDnia.loc[iGodzin, 'Zuzycie'] + Zuzycie.loc[0, iUrzadzen]

    DaneDnia.loc[:,'Wartosc zuzytej energii']  = DaneDnia.loc[:, 'Zuzycie'] * DaneDnia.loc[:, 'Cena']          
                                                                                                        # Wykres ilosci zuzytej energii i wykres wydanych pieniedzy 

    #DaneDnia.to_excel(r'C:\Users\Komputer\Desktop\del1.xlsx')

    # Porownanie zuzycia do wyprodukowanej energii
    for iSkierowanie in Kolumny_Produkcji:
        for iGodzin in range(24):
            DaneDnia.loc[iGodzin, iSkierowanie] = np.maximum(0, DaneDnia.loc[iGodzin, 'Zuzycie'] - DaneDnia.loc[iGodzin, iSkierowanie])
    
    
    IloscOstatecznieZuzytejEnergii = []
    for iSkierowanie in Kolumny_Produkcji:
        IloscOstatecznieZuzytejEnergii.append(sum(DaneDnia.loc[:, iSkierowanie]))


    #DaneDnia.to_excel(r'C:\Users\Komputer\Desktop\del2.xlsx')

    # Wyjecie najlepszych skierowan
    SkierowaniaNaNajmniejZuzytejEnergii = []
    for index, value in enumerate(IloscOstatecznieZuzytejEnergii):
        if value == min(IloscOstatecznieZuzytejEnergii):
            SkierowaniaNaNajmniejZuzytejEnergii.append(Kolumny_Produkcji[index])

    
    
    

    #Najlepsze ceny ze skierowan
    DaneDniaCena = DaneDnia
    for iSkierowanie in Kolumny_Produkcji:
        for iGodzin in range(24):
            DaneDniaCena.loc[iGodzin, iSkierowanie] = DaneDnia.loc[iGodzin, 'Cena'] * DaneDnia.loc[iGodzin, iSkierowanie]

    CenaEnergiiZPanelami = []
    for iSkierowanie in Kolumny_Produkcji:
        CenaEnergiiZPanelami.append(sum(DaneDnia.loc[:, iSkierowanie]))

    SkierowaniaNaNajmniejPieniedzy = []
    for index, value in enumerate(CenaEnergiiZPanelami):
        if value == min(CenaEnergiiZPanelami):
            SkierowaniaNaNajmniejPieniedzy.append(Kolumny_Produkcji[index])


    #Czesc wspolna dwoch skierowan powyzej
    WspolneSkierowania = list(set(SkierowaniaNaNajmniejZuzytejEnergii) & set(SkierowaniaNaNajmniejPieniedzy))

    CenaDnia = sum(DaneDnia.loc[:, 'Wartosc zuzytej energii'])

    if printy == True:
        print('Najlepsze skierowania', len(SkierowaniaNaNajmniejZuzytejEnergii), 'paneli ze wzgledu na najmniej energii pobranej z sieci: ', SkierowaniaNaNajmniejZuzytejEnergii)
        print('Najlepsze skierowania',  len(SkierowaniaNaNajmniejPieniedzy) , 'paneli ze wzgledu na najmniejsza cene energii pobranej z sieci: ', SkierowaniaNaNajmniejPieniedzy)
        print('Najlepsze skierowania', len(WspolneSkierowania), 'ogolnie: ', WspolneSkierowania)
        print('Cena za energie tego dnia (bez paneli) wynosi: ', round(CenaDnia,2), ' zl.')
        print('Dzieki uzyciu najlepszego skierowania zaoszczedzimy: ', round(CenaDnia - min(CenaEnergiiZPanelami),2),' zl.')
    else:
        return(IloscOstatecznieZuzytejEnergii, CenaEnergiiZPanelami, CenaDnia)
    

Funkcja_Dzienna('2020','12','01', Prawdopodobienstwa, printy = True)
    