# app.py

# BAZA DANYCH - Globalne listy z danymi wejściowymi
galleries_list = [
    {"nazwa": "Galeria Narodowa Zachęta", "typ_sztuki": "Sztuka współczesna", "lokalizacja": "Warszawa"},
    {"nazwa": "MOCAK", "typ_sztuki": "Sztuka nowoczesna", "lokalizacja": "Kraków"}
]

exhibitions_list = [
    {"nazwa": "Abakanowicz. Totalna", "tematyka": "Rzeźba", "lokalizacja": "Warszawa"},
    {"nazwa": "Polskie Surrealizmy", "tematyka": "Malarstwo", "lokalizacja": "Kraków"}
]

employees_list = [
    {"imie": "Jan", "nazwisko": "Kowalski", "telefon": "123456789", "stanowisko": "Kustosz",
     "miejsce": "Galeria Narodowa Zachęta", "typ_miejsca": "galeria", "dom": "Piaseczno"},
    {"imie": "Anna", "nazwisko": "Nowak", "telefon": "987654321", "stanowisko": "Przewodnik", "miejsce": "MOCAK",
     "typ_miejsca": "galeria", "dom": "Wieliczka"}
]

guests_list = [
    {"imie": "Marek", "nazwisko": "Zieliński", "telefon": "555666777", "typ_bilet": "normalny",
     "miejsce": "Galeria Narodowa Zachęta", "typ_miejsca": "galeria"},
    {"imie": "Karolina", "nazwisko": "Wiśniewska", "telefon": "444333222", "typ_bilet": "ulgowy", "miejsce": "MOCAK",
     "typ_miejsca": "galeria"}
]


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


# FUNKCJE DLA GOŚCI
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


# GŁÓWNE MENU STERUJĄCE
def main():
    while True:
        print("==========MENU==========")
        print("0 - zakończ program")
        print("1 - wyświetl dane (Galerie, Wystawy, Kadry, Goście)")
        print("2 - dodanie elementu")
        print("3 - usuwanie elementu")
        print("4 - update elementu")

        choice = input("Wybierz opcje w menu: ")
        print(f"Wybrano opcję {choice}")

        if choice == "0":
            break

        if choice == "1":
            print("\n--- GALERIE ---")
            read_galleries(galleries_list)
            print("\n--- WYSTAWY ---")
            read_exhibitions(exhibitions_list)
            print("\n--- PRACOWNICY ---")
            read_employees(employees_list)
            print("\n--- GOŚCIE ---")
            read_guests(guests_list)

        if choice == "2":
            kat = input("Co chcesz dodać? (1-galeria, 2-wystawa, 3-pracownik, 4-gość): ")
            if kat == "1": add_gallery(galleries_list)
            if kat == "2": add_exhibition(exhibitions_list)
            if kat == "3": add_employee(employees_list)
            if kat == "4": add_guest(guests_list)

        if choice == "3":
            kat = input("Co chcesz usunąć? (1-galeria, 2-wystawa, 3-pracownik, 4-gość): ")
            if kat == "1": remove_gallery(galleries_list)
            if kat == "2": remove_exhibition(exhibitions_list)
            if kat == "3": remove_employee(employees_list)
            if kat == "4": remove_guest(guests_list)

        if choice == "4":
            kat = input("Co chcesz zaktualizować? (1-galeria, 2-wystawa, 3-pracownik, 4-gość): ")
            if kat == "1": update_gallery(galleries_list)
            if kat == "2": update_exhibition(exhibitions_list)
            if kat == "3": update_employee(employees_list)
            if kat == "4": update_guest(guests_list)


if __name__ == "__main__":
    main()