# Import bibliotek
import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import calendar
from datetime import datetime
import os
import main

# Zdefiniowanie ścieżki z plikami
Sciezka = r'TomaszLysz/Symulacja_Zuzycia_Energii_i_dopasowanie_paneli_PV/tree/main'

# Nagłówek aplikacji
st.title('Aplikacja dostosowująca skierowanie paneli PV')
# Nagłowek panelu bocznego
st.sidebar.header('Wybierz szczegóły symulacji')
st.sidebar.write(os.listdir('Pliki'))
# Wybranie symulacji
Symulacja = {
    '    ':0,
    'Dzienna': 1,
    'Roczna': 2,
}
Wybrana_Symulacja = st.sidebar.selectbox('Wybierz symulację:', list(Symulacja.keys()))
# Panel boczny zależny od wybranej symulacji
if Wybrana_Symulacja == 'Dzienna' or Wybrana_Symulacja == 'Roczna':
    if st.sidebar.button('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Szczegóły modeli zużycia&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'):
            st.write('Model 1: Model domu jednorodzinnego niedostosowanego do zużycia energii w trakcie jej produkcji przez panele fotowoltaiczne. \n\n Model 2: Model domu jednorodzinnego dostosowanego do użycia energii wraz z jej produkcją przez panele fotowoltaiczne. \n\n Model 3: Model firmy z wysokim zużyciem energii w trakcie dnia (2 - zmianowy tryb pracy).')
    Model = st.sidebar.selectbox('Wybierz model zużycia:', ['1', '2', '3'])
    selected_year = st.sidebar.selectbox('Wybierz rok:', ['2018', '2019', '2020'])
    if Wybrana_Symulacja == 'Dzienna':
        selected_month = st.sidebar.selectbox('Wybierz miesiąc:', ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'])
        Miesiace = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
        # Utworzenie własnej listy nazw miesięcy w języku polskim
        polish_month_names = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
        month_index = polish_month_names.index(selected_month)

        # Wybór dni w zależności od liczby dni w miesiącu
        days_in_month = calendar.monthrange(int(selected_year), month_index + 1)[1]
        days = [str(day) for day in range(1, days_in_month + 1)]
        selected_day = st.sidebar.selectbox('Wybierz dzień:', days)
        selected_month = Miesiace.index(selected_month)+1
        selected_month = str(selected_month)
        #Wyniki = st.sidebar.checkbox('Zapisz wyniki', value = True)
        if st.sidebar.button('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;START&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'):
            current_time = datetime.now().strftime("%H:%M:%S")
            st.write('Włączenie funkcji: ', current_time)
            plt, Rezultat = main.Funkcja_main(Sciezka, selected_year, selected_month, selected_day, Wybrana_Symulacja, True, Model)
            current_time = datetime.now().strftime("%H:%M:%S")
            st.write('Koniec funkcji: ', current_time)
            st.markdown(Rezultat)
            # st.pyplot(plt)
            
    elif Wybrana_Symulacja == 'Roczna':
        selected_month = 'o'
        selected_day = 'O'
        #Wyniki = st.sidebar.checkbox('Zapisz wyniki', value = True)
        if st.sidebar.button('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;START&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'):
            current_time = datetime.now().strftime("%H:%M:%S")
            st.write('Włączenie funkcji: ', current_time)
            plt, Rezultat = main.Funkcja_main(Sciezka, selected_year, selected_month, selected_day, Wybrana_Symulacja, True, Model)
            current_time = datetime.now().strftime("%H:%M:%S")
            st.write('Koniec funkcji: ', current_time)
            st.markdown(Rezultat)
            # st.pyplot(plt)
else:
    data = None


