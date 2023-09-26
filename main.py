import tkinter as tk
from tkinter import ttk
import sqlite3
from klient import KlientScreen

root = tk.Tk()
root.title("Aplikacja do zarządzania bazą danych")

connection = sqlite3.connect('moja_baza_danych.db')
cursor = connection.cursor()

klient_screen = KlientScreen(root, connection, cursor)



root.mainloop()