# gallery_lib/controller.py

# FUNKCJE DLA GALERII SZTUKI
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


# FUNKCJE DLA WYSTAW
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


# FUNKCJE DLA PRACOWNIKÓW
def read_employees(employees):
    for i, em in enumerate(employees):
        print(f"{i} - {em['imie']} {em['nazwisko']}, Stanowisko: {em['stanowisko']}, Miejsce: {em['miejsce']}")

def add_employee(employees):
    imie = input("Imię: ")
    nazwisko = input("Nazwisko: ")
    tel = input("Telefon: ")
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
        employees[index]["telefon"] = input("Nowy telefon: ")
        employees[index]["stanowisko"] = input("Nowe stanowisko: ")
        employees[index]["miejsce"] = input("Nowe miejsce pracy: ")
        employees[index]["typ_miejsca"] = input("Nowy typ miejsca: ")
        employees[index]["dom"] = input("Nowa miejscowość zamieszkania: ")


# FUNKCJE DLA GOŚCIE
def read_guests(guests):
    for i, g in enumerate(guests):
        print(f"{i} - {g['imie']} {g['nazwisko']}, Bilet: {g['typ_bilet']}, Cel: {g['miejsce']}")

def add_guest(guests):
    imie = input("Imię: ")
    nazwisko = input("Nazwisko: ")
    tel = input("Telefon: ")
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
        guests[index]["telefon"] = input("Nowy telefon: ")
        guests[index]["typ_bilet"] = input("Nowy typ biletu: ")
        guests[index]["miejsce"] = input("Nowe miejsce wizyty: ")
        guests[index]["typ_miejsca"] = input("Nowy typ miejsca: ")