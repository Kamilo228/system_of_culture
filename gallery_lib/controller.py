import gallery_lib.model as model

#  FUNKCJE DLA GALERII
def add_gallery(galleries_list: list, name: str, art_type: str, location: str):
    if not name or not location: return None
    new_g = model.Gallery(name, art_type, location)
    galleries_list.append(new_g)
    return new_g

def remove_gallery(galleries_list: list, index: int):
    if 0 <= index < len(galleries_list):
        return galleries_list.pop(index)
    return None

def update_gallery(galleries_list: list, index: int, name: str, art_type: str, location: str):
    if 0 <= index < len(galleries_list):
        g = galleries_list[index]
        g.nazwa = name
        g.typ_sztuki = art_type
        g.lokalizacja = location
        g.coordinates = g.get_coordinates()
        return g
    return None


#  FUNKCJE DLA WYSTAW
def add_exhibition(exhibitions_list: list, name: str, topic: str, location: str):
    if not name or not location: return None
    new_ex = model.Exhibition(name, topic, location)
    exhibitions_list.append(new_ex)
    return new_ex

def remove_exhibition(exhibitions_list: list, index: int):
    if 0 <= index < len(exhibitions_list):
        return exhibitions_list.pop(index)
    return None

def update_exhibition(exhibitions_list: list, index: int, name: str, topic: str, location: str):
    if 0 <= index < len(exhibitions_list):
        ex = exhibitions_list[index]
        ex.nazwa = name
        ex.tematyka = topic
        ex.lokalizacja = location
        ex.coordinates = ex.get_coordinates()
        return ex
    return None


#  FUNKCJE DLA PRACOWNIKÓW
def add_employee(employees_list: list, imie, nazwisko, tel, stanowisko, miejsce, typ_miejsca, dom):
    if not imie or not nazwisko: return None
    new_emp = model.Employee(imie, nazwisko, tel, stanowisko, miejsce, typ_miejsca, dom)
    employees_list.append(new_emp)
    return new_emp

def remove_employee(employees_list: list, index: int):
    if 0 <= index < len(employees_list):
        return employees_list.pop(index)
    return None

def update_employee(employees_list: list, index: int, imie, nazwisko, tel, stanowisko, miejsce, typ_miejsca, dom):
    if 0 <= index < len(employees_list):
        emp = employees_list[index]
        emp.imie = imie
        emp.nazwisko = nazwisko
        emp.telefon = tel
        emp.stanowisko = stanowisko
        emp.miejsce = miejsce
        emp.typ_miejsca = typ_miejsca
        emp.dom = dom
        emp.coordinates = emp.get_coordinates()
        return emp
    return None


#  FUNKCJE DLA GOŚCI
def add_guest(guests_list: list, imie, nazwisko, tel, bilet, miejsce, typ_miejsca):
    if not imie or not nazwisko: return None
    new_gst = model.Guest(imie, nazwisko, tel, bilet, miejsce, typ_miejsca)
    guests_list.append(new_gst)
    return new_gst

def remove_guest(guests_list: list, index: int):
    if 0 <= index < len(guests_list):
        return guests_list.pop(index)
    return None

def update_guest(guests_list: list, index: int, imie, nazwisko, tel, bilet, miejsce, typ_miejsca):
    if 0 <= index < len(guests_list):
        gst = guests_list[index]
        gst.imie = imie
        gst.nazwisko = nazwisko
        gst.telefon = tel
        gst.typ_bilet = bilet
        gst.miejsce = miejsce
        gst.typ_miejsca = typ_miejsca
        return gst
    return None

