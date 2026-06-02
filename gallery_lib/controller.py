# gallery_lib/controller.py
from bs4 import BeautifulSoup
import requests
import folium

# --- GALERIE ---
def read_galleries(galleries):
    for i, g in enumerate(galleries):
        print(f"{i} - {g['nazwa']}, Typ: {g['typ_sztuki']}, Lokalizacja: {g['lokalizacja']}")

def add_gallery(galleries):
    name = input("Podaj nazwę galerii: ")
    art_type = input("Podaj typ sztuki: ")
    location = input("Podaj miasto: ")
    new_g = {"nazwa": name, "typ_sztuki": art_type, "lokalizacja": location}
    galleries.append(new_g)

def remove_gallery(galleries):
    read_galleries(galleries)
    index = int(input("Wybierz indeks galerii do usunięcia: "))
    if 0 <= index < len(galleries):
        galleries.pop(index)

def update_gallery(galleries):
    read_galleries(galleries)
    index = int(input("Wybierz indeks galerii do edycji: "))
    if 0 <= index < len(galleries):
        galleries[index]["nazwa"] = input("Podaj nową nazwę: ")
        galleries[index]["typ_sztuki"] = input("Podaj nowy typ sztuki: ")
        galleries[index]["lokalizacja"] = input("Podaj nową lokalizację: ")

# --- WYSTAWY ---
def read_exhibitions(exhibitions):
    for i, e in enumerate(exhibitions):
        print(f"{i} - {e['nazwa']}, Tematyka: {e['tematyka']}, Lokalizacja: {e['lokalizacja']}")

def add_exhibition(exhibitions):
    name = input("Podaj nazwę wystawy: ")
    topic = input("Podaj tematykę: ")
    location = input("Podaj miasto: ")
    new_e = {"nazwa": name, "tematyka": topic, "lokalizacja": location}
    exhibitions.append(new_e)

def remove_exhibition(exhibitions):
    read_exhibitions(exhibitions)
    index = int(input("Wybierz indeks wystawy do usunięcia: "))
    if 0 <= index < len(exhibitions):
        exhibitions.pop(index)

def update_exhibition(exhibitions):
    read_exhibitions(exhibitions)
    index = int(input("Wybierz indeks wystawy do edycji: "))
    if 0 <= index < len(exhibitions):
        exhibitions[index]["nazwa"] = input("Podaj nową nazwę: ")
        exhibitions[index]["tematyka"] = input("Podaj nową tematykę: ")
        exhibitions[index]["lokalizacja"] = input("Podaj nową lokalizację: ")

# --- PRACOWNICY ---
def read_employees(employees):
    for i, em in enumerate(employees):
        print(f"{i} - {em['imie']} {em['nazwisko']}, Tel: {em['telefon']}, Stanowisko: {em['stanowisko']}")

def add_employee(employees):
    imie = input("Imię: ")
    nazwisko = input("Nazwisko: ")
    tel = input("Numer telefonu (format 000-000-000): ")
    stanowisko = input("Stanowisko: ")
    miejsce = input("Miejsce pracy: ")
    typ_miejsca = input("Typ miejsca (galeria/wystawa): ")
    dom = input("Miejscowość zamieszkania: ")
    new_emp = {
        "imie": imie, "nazwisko": nazwisko, "telefon": tel,
        "stanowisko": stanowisko, "miejsce": miejsce,
        "typ_miejsca": typ_miejsca, "dom": dom
    }
    employees.append(new_emp)

def remove_employee(employees):
    read_employees(employees)
    index = int(input("Wybierz indeks pracownika do usunięcia: "))
    if 0 <= index < len(employees):
        employees.pop(index)

def update_employee(employees):
    read_employees(employees)
    index = int(input("Wybierz indeks pracownika do edycji: "))
    if 0 <= index < len(employees):
        employees[index]["imie"] = input("Nowe imię: ")
        employees[index]["nazwisko"] = input("Nowe nazwisko: ")
        employees[index]["telefon"] = input("Nowy numer telefonu (format 000-000-000): ")
        employees[index]["stanowisko"] = input("Nowe stanowisko: ")
        employees[index]["miejsce"] = input("Nowe miejsce pracy: ")
        employees[index]["typ_miejsca"] = input("Nowy typ miejsca: ")
        employees[index]["dom"] = input("Nowa miejscowość zamieszkania: ")

# --- GOŚCIE ---
def read_guests(guests):
    for i, g in enumerate(guests):
        print(f"{i} - {g['imie']} {g['nazwisko']}, Tel: {g['telefon']}, Bilet: {g['typ_bilet']}")

def add_guest(guests):
    imie = input("Imię: ")
    nazwisko = input("Nazwisko: ")
    tel = input("Numer telefonu (format 000-000-000): ")
    bilet = input("Typ biletu: ")
    miejsce = input("Miejsce wizyty: ")
    typ_miejsca = input("Typ miejsca (galeria/wystawa): ")
    new_g = {
        "imie": imie, "nazwisko": nazwisko, "telefon": tel,
        "typ_bilet": bilet, "miejsce": miejsce, "typ_miejsca": typ_miejsca
    }
    guests.append(new_g)

def remove_guest(guests):
    read_guests(guests)
    index = int(input("Wybierz indeks gościa do usunięcia: "))
    if 0 <= index < len(guests):
        guests.pop(index)

def update_guest(guests):
    read_guests(guests)
    index = int(input("Wybierz indeks gościa do edycji: "))
    if 0 <= index < len(guests):
        guests[index]["imie"] = input("Nowe imię: ")
        guests[index]["nazwisko"] = input("Nowe nazwisko: ")
        guests[index]["telefon"] = input("Nowy numer telefonu (format 000-000-000): ")
        guests[index]["typ_bilet"] = input("Nowy typ biletu: ")
        guests[index]["miejsce"] = input("Nowe miejsce wizyty: ")
        guests[index]["typ_miejsca"] = input("Nowy typ miejsca: ")


def get_coordinates(location: str) -> list:
    url = f"https://pl.wikipedia.org/wiki/{location}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response_html = BeautifulSoup(response.text, 'html.parser')
    latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
    longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
    return [latitude, longitude]


def get_map(galleries: list, exhibitions: list) -> None:
    m = folium.Map([52.23, 21], zoom_start=6)

    # Mapowanie galerii
    for g in galleries:
        folium.Marker(
            location=get_coordinates(g["lokalizacja"]),
            tooltip=g["nazwa"],
            popup=g["typ_sztuki"],
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)

    # Mapowanie wystaw
    for e in exhibitions:
        folium.Marker(
            location=get_coordinates(e["lokalizacja"]),
            tooltip=e["nazwa"],
            popup=e["tematyka"],
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)

    m.save("mapa_lokalizacji.html")
    print("Mapa została pomyślnie wygenerowana i zapisana jako: mapa_lokalizacji.html")