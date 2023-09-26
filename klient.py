import tkinter as tk
from tkinter import ttk
import sqlite3
import re
import csv
from tkinter import filedialog

class KlientScreen:
    def __init__(self, root, connection, cursor):
        self.root = root
        self.connection = connection
        self.cursor = cursor

        self.frame_dodawanie = ttk.LabelFrame(root, text="Dodawanie Rekordu")
        self.frame_dodawanie.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.frame_edycja = ttk.LabelFrame(root, text="Edycja Rekordu")
        self.frame_edycja.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.frame_lista = ttk.LabelFrame(root, text="Lista Rekordów")
        self.frame_lista.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.frame_filtr = ttk.LabelFrame(root, text="Filtrowanie Rekordów")
        self.frame_filtr.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.button_eksportuj = ttk.Button(self.frame_filtr, text="Eksportuj do CSV", command=self.generuj_plik_csv)
        self.button_eksportuj.grid(row=5, column=0, columnspan=5, padx=5, pady=5)

        self.button_wczytaj = ttk.Button(self.frame_filtr, text="Wczytaj z pliku CSV", command=self.wczytaj_z_pliku_csv)
        self.button_wczytaj.grid(row=6, column=0, columnspan=5, padx=5, pady=5)

        self.label_imie = ttk.Label(self.frame_dodawanie, text="Imie:")
        self.label_imie.grid(row=0, column=0, padx=5, pady=5)
        self.entry_imie = ttk.Entry(self.frame_dodawanie)
        self.entry_imie.grid(row=0, column=1, padx=5, pady=5)

        self.label_nazwisko = ttk.Label(self.frame_dodawanie, text="Nazwisko:")
        self.label_nazwisko.grid(row=1, column=0, padx=5, pady=5)
        self.entry_nazwisko = ttk.Entry(self.frame_dodawanie)
        self.entry_nazwisko.grid(row=1, column=1, padx=5, pady=5)

        self.label_wiek = ttk.Label(self.frame_dodawanie, text="Wiek:")
        self.label_wiek.grid(row=2, column=0, padx=5, pady=5)
        self.entry_wiek = ttk.Entry(self.frame_dodawanie)
        self.entry_wiek.grid(row=2, column=1, padx=5, pady=5)

        self.button_dodaj = ttk.Button(self.frame_dodawanie, text="Dodaj", command=self.dodaj_rekord)
        self.button_dodaj.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.button_usun = ttk.Button(self.frame_edycja, text="Usuń", command=self.usun_rekord)
        self.button_usun.grid(row=0, column=0, padx=5, pady=5)

        self.button_edytuj = ttk.Button(self.frame_edycja, text="Edytuj", command=self.edytuj_rekord)
        self.button_edytuj.grid(row=0, column=1, padx=5, pady=5)

        self.treeview = ttk.Treeview(self.frame_lista, columns=('ID', 'Imie', 'Nazwisko', 'Wiek'), show='headings')
        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Imie', text='Imie')
        self.treeview.heading('Nazwisko', text='Nazwisko')
        self.treeview.heading('Wiek', text='Wiek')
        self.treeview.pack(fill='both', expand=True)
        self.treeview.bind('<ButtonRelease-1>', self.wybierz_rekord)

        self.label_wyszukaj_imie = ttk.Label(self.frame_filtr, text="Wyszukaj Imię:")
        self.label_wyszukaj_imie.grid(row=0, column=0, padx=5, pady=5)
        self.entry_wyszukaj_imie = ttk.Entry(self.frame_filtr)
        self.entry_wyszukaj_imie.grid(row=0, column=1, padx=5, pady=5)

        self.label_wyszukaj_nazwisko = ttk.Label(self.frame_filtr, text="Wyszukaj Nazwisko:")
        self.label_wyszukaj_nazwisko.grid(row=1, column=0, padx=5, pady=5)
        self.entry_wyszukaj_nazwisko = ttk.Entry(self.frame_filtr)
        self.entry_wyszukaj_nazwisko.grid(row=1, column=1, padx=5, pady=5)

        self.button_wyszukaj = ttk.Button(self.frame_filtr, text="Wyszukaj", command=self.wyszukaj_rekordy)
        self.button_wyszukaj.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.combo_sortowanie = ttk.Combobox(self.frame_filtr, values=['ID', 'Imie', 'Nazwisko', 'Wiek'])
        self.combo_sortowanie.set('ID')
        self.combo_sortowanie.grid(row=3, column=0, padx=5, pady=5)

        self.button_sortuj = ttk.Button(self.frame_filtr, text="Sortuj", command=self.sortuj_rekordy)
        self.button_sortuj.grid(row=3, column=1, padx=5, pady=5)

        self.label_filtr_wiek = ttk.Label(self.frame_filtr, text="Filtr wieku:")
        self.label_filtr_wiek.grid(row=4, column=0, padx=5, pady=5)
        self.entry_filtr_wiek_min = ttk.Entry(self.frame_filtr, width=5)
        self.entry_filtr_wiek_min.grid(row=4, column=1, padx=5, pady=5)
        self.label_do = ttk.Label(self.frame_filtr, text="do")
        self.label_do.grid(row=4, column=2, padx=5, pady=5)
        self.entry_filtr_wiek_max = ttk.Entry(self.frame_filtr, width=5)
        self.entry_filtr_wiek_max.grid(row=4, column=3, padx=5, pady=5)

        self.button_filtruj = ttk.Button(self.frame_filtr, text="Filtruj", command=self.filtruj_rekordy)
        self.button_filtruj.grid(row=4, column=4, padx=5, pady=5)

        self.aktualizuj_liste()

        

        # Inicjalizuj interfejs dla klientów
        self.initialize_ui()

    def initialize_ui(self):

        # Inicjalizacja bazy danych
        connection = sqlite3.connect('moja_baza_danych.db')
        cursor = connection.cursor()

        # Tworzenie tabeli, jeśli nie istnieje
        cursor.execute('''CREATE TABLE IF NOT EXISTS moja_tabela 
                          (id INTEGER PRIMARY KEY, imie TEXT, nazwisko TEXT, wiek INTEGER)''')
        connection.commit()      
        
    def generuj_plik_csv(self):
        
        with open("klienci.csv", 'w', newline='', encoding='utf-8') as csvfile:
            # Utwórz writer
            writer = csv.writer(csvfile)
            self.cursor.execute("SELECT * FROM moja_tabela")
            wyniki = self.cursor.fetchall()
            # Zapisz nagłówki (kolumny)
            writer.writerow(['ID', 'Imię', 'Nazwisko', 'Wiek'])  # Zastanów się, czy masz nazwy kolumn takie jak te
            # Zapisz rekordy
            for rekord in wyniki:
                writer.writerow(rekord)

    def wczytaj_z_pliku_csv(self):
        nazwa_pliku = filedialog.askopenfilename(filetypes=[('Pliki CSV', '*.csv')])
        if not nazwa_pliku:
            return  # Użytkownik anulował wybór pliku

        # Usunięcie wszystkich rekordów z tabeli
        self.cursor.execute("DELETE FROM moja_tabela")
        self.connection.commit()

        # Dodanie rekordów z pliku do bazy danych
        with open(nazwa_pliku, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Pominięcie nagłówków

            for row in reader:
                Id,imie, nazwisko, wiek = row

                # Dodawanie rekordu do bazy danych
                self.cursor.execute("INSERT INTO moja_tabela (id,imie, nazwisko, wiek) VALUES (?,?, ?, ?)", (Id,imie, nazwisko, wiek))
                self.connection.commit()

        self.aktualizuj_liste()  # Aktualizuj listę po wczytaniu danych

    def dodaj_rekord(self):
        imie = self.entry_imie.get()
        nazwisko = self.entry_nazwisko.get()
        wiek = self.entry_wiek.get()
        # Dodawanie rekordu do bazy danych
        if int(wiek) >= 18:
            self.cursor.execute("INSERT INTO moja_tabela (imie, nazwisko, wiek) VALUES (?, ?, ?)", (imie, nazwisko, wiek))
            self.connection.commit()
            self.aktualizuj_liste()

    def usun_rekord(self):
        selected_item = self.treeview.focus()
        if selected_item:
            rekord_name = self.treeview.item(selected_item)['values']
            rekord_id = rekord_name[0]

            self.cursor.execute("DELETE FROM moja_tabela WHERE id=?", (rekord_id,))
            self.connection.commit()
            self.aktualizuj_liste()

    def edytuj_rekord(self):
        selected_item = self.treeview.focus()
        if selected_item:
            rekord_name = self.treeview.item(selected_item)['values']
            rekord_id = rekord_name[0]
            imie = self.entry_imie.get()
            nazwisko = self.entry_nazwisko.get()
            wiek = self.entry_wiek.get()

            self.cursor.execute("UPDATE moja_tabela SET imie=?, nazwisko=?, wiek=? WHERE id=?", (imie, nazwisko, wiek, rekord_id))
            self.connection.commit()
            self.aktualizuj_liste()

    def wybierz_rekord(self,event):
        selected_item = self.treeview.focus()
        if selected_item:
            rekord_name = self.treeview.item(selected_item)['values']
            rekord_id = rekord_name[0]

            print(rekord_name)
            self.cursor.execute("SELECT * FROM moja_tabela WHERE id=?", (rekord_id,))
            rekord = self.cursor.fetchone()
            if rekord:
                self.entry_imie.delete(0, tk.END)
                self.entry_nazwisko.delete(0, tk.END)
                self.entry_wiek.delete(0, tk.END)
                self.entry_imie.insert(0, rekord[1])
                self.entry_nazwisko.insert(0, rekord[2])
                self.entry_wiek.insert(0, rekord[3])

    def wyszukaj_rekordy(self):
        imie = self.entry_wyszukaj_imie.get()
        nazwisko = self.entry_wyszukaj_nazwisko.get()
        self.cursor.execute("SELECT * FROM moja_tabela WHERE imie LIKE ? AND nazwisko LIKE ?", ('%' + imie + '%', '%' + nazwisko + '%'))
        wyniki = self.cursor.fetchall()
        self.aktualizuj_liste(wyniki)

    def sortuj_rekordy(self):
        kolumna = self.combo_sortowanie.get()
        self.cursor.execute(f"SELECT * FROM moja_tabela ORDER BY {kolumna}")
        wyniki = self.cursor.fetchall()
        self.aktualizuj_liste(wyniki)

    def filtruj_rekordy(self):
        wiek_min = self.entry_filtr_wiek_min.get()
        wiek_max = self.entry_filtr_wiek_max.get()
        self.cursor.execute("SELECT * FROM moja_tabela WHERE wiek BETWEEN ? AND ?", (wiek_min, wiek_max))
        wyniki = self.cursor.fetchall()
        self.aktualizuj_liste(wyniki)

    def aktualizuj_liste(self,wyniki=None):
        if not wyniki:
            self.cursor.execute("SELECT * FROM moja_tabela")
            wyniki = self.cursor.fetchall()
        self.treeview.delete(*self.treeview.get_children())

        for rekord in wyniki:
            self.treeview.insert('', 'end', values=rekord)