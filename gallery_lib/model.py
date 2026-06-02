import requests
from bs4 import BeautifulSoup

class Gallery:
    def __init__(self, nazwa: str, typ_sztuki: str, lokalizacja: str):
        self.nazwa = nazwa
        self.typ_sztuki = typ_sztuki
        self.lokalizacja = lokalizacja
        self.coordinates = self.get_coordinates()

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response_html = BeautifulSoup(response.text, 'html.parser')
            latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
            longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
            return [round(latitude, 4), round(longitude, 4)]
        except Exception:
            return [52.2297, 21.0122]

class Exhibition:
    def __init__(self, nazwa: str, tematyka: str, lokalizacja: str):
        self.nazwa = nazwa
        self.tematyka = tematyka
        self.lokalizacja = lokalizacja
        self.coordinates = self.get_coordinates()

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response_html = BeautifulSoup(response.text, 'html.parser')
            latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
            longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
            return [round(latitude, 4), round(longitude, 4)]
        except Exception:
            return [52.2297, 21.0122]

class Employee:
    def __init__(self, imie: str, nazwisko: str, telefon: str, stanowisko: str, miejsce: str, typ_miejsca: str, dom: str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.telefon = telefon
        self.stanowisko = stanowisko
        self.miejsce = miejsce
        self.typ_miejsca = typ_miejsca
        self.dom = dom
        self.coordinates = self.get_coordinates()

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.dom}"
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response_html = BeautifulSoup(response.text, 'html.parser')
            latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
            longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
            return [round(latitude, 4), round(longitude, 4)]
        except Exception:
            return [52.2297, 21.0122]

class Guest:
    def __init__(self, imie: str, nazwisko: str, telefon: str, typ_bilet: str, miejsce: str, typ_miejsca: str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.telefon = telefon
        self.typ_bilet = typ_bilet
        self.miejsce = miejsce
        self.typ_miejsca = typ_miejsca

galleries = [
    Gallery("Galeria Zachęta", "Sztuka", "Warszawa"),
    Gallery("MOCAK", "Sztuka Współczesna", "Kraków")
]

exhibitions = [
    Exhibition("Złoty Wiek Gdańska", "Malarstwo Historyczne", "Gdańsk"),
    Exhibition("Beksiński Nieznany", "Surrealizm", "Wrocław")
]

employees = [
    Employee("Jan", "Kowalski", "501-234-567", "Kustosz", "Galeria Zachęta", "galeria", "Poznań"),
    Employee("Anna", "Nowak", "699-888-777", "Przewodnik", "Beksiński Nieznany", "wystawa", "Zakopane")
]

guests = [
    Guest("Marek", "Podróżnik", "732-111-222", "Normalny", "Galeria Zachęta", "galeria"),
    Guest("Kasia", "Sztukofil", "605-444-333", "Ulgowy", "Beksiński Nieznany", "wystawa")
]