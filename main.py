from tkinter import *
from tkinter import ttk
import tkintermapview

# Import modelu oraz funkcji kontrolera
import gallery_lib.model as model
from gallery_lib.controller import (
    add_gallery, remove_gallery, update_gallery,
    add_exhibition, remove_exhibition, update_exhibition,
    add_employee, remove_employee, update_employee,
    add_guest, remove_guest, update_guest
)


class ApplicationWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("System Kultury")
        self.root.geometry("1024x760")

        # Słownik do zarządzania referencjami markerów
        self.markers = {}

        self.build_gui()

        # USTAWIENIE MAPY NA ŚRODEK POLSKI
        self.center_maps_on_poland()

        self.rebuild_all_markers_on_startup()
        self.refresh_all_views()

    def center_maps_on_poland(self):
        # Współrzędne geometrycznego środka Polski i optymalny zoom (6), by objąć cały kraj
        srodek_pl_lat, srodek_pl_lon = 52.1130, 19.4236
        zoom_pl = 6

        self.map_widget_g.set_position(srodek_pl_lat, srodek_pl_lon)
        self.map_widget_g.set_zoom(zoom_pl)

        self.map_widget_ex.set_position(srodek_pl_lat, srodek_pl_lon)
        self.map_widget_ex.set_zoom(zoom_pl)

        self.map_widget_emp.set_position(srodek_pl_lat, srodek_pl_lon)
        self.map_widget_emp.set_zoom(zoom_pl)

    def build_gui(self):
        main_notebook = ttk.Notebook(self.root)
        main_notebook.pack(fill="both", expand=True, padx=10, pady=10)

        ramka_tab_galerie = Frame(main_notebook)
        ramka_tab_wystawy = Frame(main_notebook)
        ramka_tab_kadry = Frame(main_notebook)

        main_notebook.add(ramka_tab_galerie, text='   Galerie Sztuki   ')
        main_notebook.add(ramka_tab_wystawy, text='   Wystawy   ')
        main_notebook.add(ramka_tab_kadry, text=' Panel Zarządzania Pracownikami i Gośćmi   ')


        # ZAKŁADKA 1: GALERIE SZTUKI

        ramka_g_gora = Frame(ramka_tab_galerie);
        ramka_g_gora.pack(side=TOP, fill=X, padx=15, pady=5)
        ramka_g_lewa = Frame(ramka_g_gora);
        ramka_g_lewa.pack(side=LEFT, fill=Y)

        ramka_g_formularz = LabelFrame(ramka_g_lewa, text=" Dodaj / Edytuj Galerię ", padx=10, pady=10)
        ramka_g_formularz.pack(fill=X, pady=5)
        Label(ramka_g_formularz, text="Nazwa:").grid(row=0, column=0, sticky=W, pady=2)
        self.entry_g_nazwa = Entry(ramka_g_formularz, width=28);
        self.entry_g_nazwa.grid(row=0, column=1, pady=2)
        Label(ramka_g_formularz, text="Typ sztuki:").grid(row=1, column=0, sticky=W, pady=2)
        self.entry_g_typ = Entry(ramka_g_formularz, width=28);
        self.entry_g_typ.grid(row=1, column=1, pady=2)
        Label(ramka_g_formularz, text="Miasto:").grid(row=2, column=0, sticky=W, pady=2)
        self.entry_g_lok = Entry(ramka_g_formularz, width=28);
        self.entry_g_lok.grid(row=2, column=1, pady=2)

        self.button_g_akcja = Button(ramka_g_formularz, text="Dodaj galerię", command=self.gui_add_gallery,
                                     bg="#d4edda")
        self.button_g_akcja.grid(row=3, column=0, columnspan=2, pady=8)

        Label(ramka_g_lewa, text="Lista Galerii:").pack(anchor=W, pady=(5, 2))
        self.listbox_galerie = Listbox(ramka_g_lewa, width=44, height=11)
        self.listbox_galerie.pack(fill=X)
        self.listbox_galerie.bind("<<ListboxSelect>>", self.gui_on_gallery_selected)

        ramka_g_przyciski = Frame(ramka_g_lewa);
        ramka_g_przyciski.pack(fill=X, pady=5)
        Button(ramka_g_przyciski, text="Pokaż szczegóły", command=self.gui_show_gallery_details, bg="#cce5ff").pack(
            fill=X, pady=2)
        Button(ramka_g_przyciski, text="Edytuj", command=self.gui_edit_gallery).pack(side=LEFT, expand=True, fill=X,
                                                                                     padx=2, pady=2)
        Button(ramka_g_przyciski, text="Usuń", command=self.gui_remove_gallery, fg="red").pack(side=LEFT, expand=True,
                                                                                               fill=X, padx=2, pady=2)

        ramka_g_prawa = Frame(ramka_g_gora);
        ramka_g_prawa.pack(side=RIGHT, fill="both", expand=True, padx=(15, 0))
        self.map_widget_g = tkintermapview.TkinterMapView(ramka_g_prawa, corner_radius=10, height=330)
        self.map_widget_g.pack(fill="both", expand=True, pady=5)

        ramka_g_dol = Frame(ramka_tab_galerie);
        ramka_g_dol.pack(side=BOTTOM, fill="both", expand=True, padx=15, pady=5)
        self.label_g_tytul_sekcji = Label(ramka_g_dol,
                                          text="Szczegóły obiektu: (Wybierz galerię i kliknij 'Pokaż szczegóły')",
                                          font=("Arial", 10, "italic", "bold"), fg="#333333")
        self.label_g_tytul_sekcji.pack(anchor=W, pady=(0, 5))

        ramka_g_tabele_siatka = Frame(ramka_g_dol);
        ramka_g_tabele_siatka.pack(fill="both", expand=True)
        ramka_g_tabele_siatka.columnconfigure(0, weight=1, uniform="grupa_g");
        ramka_g_tabele_siatka.columnconfigure(1, weight=1, uniform="grupa_g")

        # TABELA 1: PRACOWNICY GALERII (Równe i rozciągliwe kolumny)
        ramka_g_kolumna_pracownicy = Frame(ramka_g_tabele_siatka);
        ramka_g_kolumna_pracownicy.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        Label(ramka_g_kolumna_pracownicy, text="Pracownicy galerii:", font=("Arial", 9, "bold")).pack(anchor=W)
        self.treeview_g_pracownicy = ttk.Treeview(ramka_g_kolumna_pracownicy,
                                                  columns=("Imie", "Nazwisko", "Telefon", "Stanowisko", "Dom"),
                                                  show="headings", height=8)

        self.treeview_g_pracownicy.heading("Imie", text="Imię");
        self.treeview_g_pracownicy.heading("Nazwisko", text="Nazwisko");
        self.treeview_g_pracownicy.heading("Telefon", text="Telefon");
        self.treeview_g_pracownicy.heading("Stanowisko", text="Stanowisko");
        self.treeview_g_pracownicy.heading("Dom", text="Msc Zamieszkania")
        for col in ("Imie", "Nazwisko", "Telefon", "Stanowisko", "Dom"):
            self.treeview_g_pracownicy.column(col, width=100, minwidth=50, stretch=True, anchor=CENTER)
        self.treeview_g_pracownicy.pack(fill="both", expand=True, pady=2)

        # TABELA 2: GOŚCIE GALERII (Równe i rozciągliwe kolumny)
        ramka_g_kolumna_goscie = Frame(ramka_g_tabele_siatka);
        ramka_g_kolumna_goscie.grid(row=0, column=1, sticky="nsew")
        Label(ramka_g_kolumna_goscie, text="Goście galerii:", font=("Arial", 9, "bold")).pack(anchor=W)
        self.treeview_g_goscie = ttk.Treeview(ramka_g_kolumna_goscie, columns=("Imie", "Nazwisko", "Telefon", "Bilet"),
                                              show="headings", height=8)

        self.treeview_g_goscie.heading("Imie", text="Imię");
        self.treeview_g_goscie.heading("Nazwisko", text="Nazwisko");
        self.treeview_g_goscie.heading("Telefon", text="Telefon");
        self.treeview_g_goscie.heading("Bilet", text="Typ Biletu")
        for col in ("Imie", "Nazwisko", "Telefon", "Bilet"):
            self.treeview_g_goscie.column(col, width=100, minwidth=50, stretch=True, anchor=CENTER)
        self.treeview_g_goscie.pack(fill="both", expand=True, pady=2)


        # ZAKŁADKA 2: WYSTAWY

        ramka_ex_gora = Frame(ramka_tab_wystawy);
        ramka_ex_gora.pack(side=TOP, fill=X, padx=15, pady=5)
        ramka_ex_lewa = Frame(ramka_ex_gora);
        ramka_ex_lewa.pack(side=LEFT, fill=Y)

        ramka_ex_formularz = LabelFrame(ramka_ex_lewa, text=" Dodaj / Edytuj Wystawę ", padx=10, pady=10)
        ramka_ex_formularz.pack(fill=X, pady=5)
        Label(ramka_ex_formularz, text="Nazwa:").grid(row=0, column=0, sticky=W, pady=2)
        self.entry_ex_nazwa = Entry(ramka_ex_formularz, width=28);
        self.entry_ex_nazwa.grid(row=0, column=1, pady=2)
        Label(ramka_ex_formularz, text="Tematyka:").grid(row=1, column=0, sticky=W, pady=2)
        self.entry_ex_temat = Entry(ramka_ex_formularz, width=28);
        self.entry_ex_temat.grid(row=1, column=1, pady=2)
        Label(ramka_ex_formularz, text="Miasto:").grid(row=2, column=0, sticky=W, pady=2)
        self.entry_ex_lok = Entry(ramka_ex_formularz, width=28);
        self.entry_ex_lok.grid(row=2, column=1, pady=2)
        self.button_ex_akcja = Button(ramka_ex_formularz, text="Dodaj wystawę", command=self.gui_add_exhibition,
                                      bg="#d4edda")
        self.button_ex_akcja.grid(row=3, column=0, columnspan=2, pady=8)

        Label(ramka_ex_lewa, text="Lista Wystaw:").pack(anchor=W, pady=(5, 2))
        self.listbox_wystawy = Listbox(ramka_ex_lewa, width=44, height=11)
        self.listbox_wystawy.pack(fill=X)
        self.listbox_wystawy.bind("<<ListboxSelect>>", self.gui_on_exhibition_selected)

        ramka_ex_przyciski = Frame(ramka_ex_lewa);
        ramka_ex_przyciski.pack(fill=X, pady=5)
        Button(ramka_ex_przyciski, text="🔎 Pokaż szczegóły", command=self.gui_show_exhibition_details,
               bg="#cce5ff").pack(fill=X, pady=2)
        Button(ramka_ex_przyciski, text="Edytuj", command=self.gui_edit_exhibition).pack(side=LEFT, expand=True, fill=X,
                                                                                         padx=2, pady=2)
        Button(ramka_ex_przyciski, text="Usuń", command=self.gui_remove_exhibition, fg="red").pack(side=LEFT,
                                                                                                   expand=True, fill=X,
                                                                                                   padx=2, pady=2)

        ramka_ex_prawa = Frame(ramka_ex_gora);
        ramka_ex_prawa.pack(side=RIGHT, fill="both", expand=True, padx=(15, 0))
        self.map_widget_ex = tkintermapview.TkinterMapView(ramka_ex_prawa, corner_radius=10, height=330)
        self.map_widget_ex.pack(fill="both", expand=True, pady=5)

        ramka_ex_dol = Frame(ramka_tab_wystawy);
        ramka_ex_dol.pack(side=BOTTOM, fill="both", expand=True, padx=15, pady=5)
        self.label_ex_tytul_sekcji = Label(ramka_ex_dol,
                                           text="Szczegóły obiektu: (Wybierz wystawę i kliknij 'Pokaż szczegóły')",
                                           font=("Arial", 10, "italic", "bold"), fg="#333333")
        self.label_ex_tytul_sekcji.pack(anchor=W, pady=(0, 5))

        ramka_ex_tabele_siatka = Frame(ramka_ex_dol);
        ramka_ex_tabele_siatka.pack(fill="both", expand=True)
        ramka_ex_tabele_siatka.columnconfigure(0, weight=1, uniform="grupa_ex");
        ramka_ex_tabele_siatka.columnconfigure(1, weight=1, uniform="grupa_ex")

        # TABELA 3: PRACOWNICY WYSTAWY
        ramka_ex_kolumna_pracownicy = Frame(ramka_ex_tabele_siatka);
        ramka_ex_kolumna_pracownicy.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        Label(ramka_ex_kolumna_pracownicy, text="Pracownicy wystawy:", font=("Arial", 9, "bold")).pack(anchor=W)
        self.treeview_ex_pracownicy = ttk.Treeview(ramka_ex_kolumna_pracownicy,
                                                   columns=("Imie", "Nazwisko", "Telefon", "Stanowisko", "Dom"),
                                                   show="headings", height=8)

        self.treeview_ex_pracownicy.heading("Imie", text="Imię");
        self.treeview_ex_pracownicy.heading("Nazwisko", text="Nazwisko");
        self.treeview_ex_pracownicy.heading("Telefon", text="Telefon");
        self.treeview_ex_pracownicy.heading("Stanowisko", text="Stanowisko");
        self.treeview_ex_pracownicy.heading("Dom", text="Msc Zamieszkania")
        for col in ("Imie", "Nazwisko", "Telefon", "Stanowisko", "Dom"):
            self.treeview_ex_pracownicy.column(col, width=100, minwidth=50, stretch=True, anchor=CENTER)
        self.treeview_ex_pracownicy.pack(fill="both", expand=True, pady=2)

        # TABELA 4: GOŚCIE WYSTAWY
        ramka_ex_kolumna_goscie = Frame(ramka_ex_tabele_siatka);
        ramka_ex_kolumna_goscie.grid(row=0, column=1, sticky="nsew")
        Label(ramka_ex_kolumna_goscie, text="Goście wystawy:", font=("Arial", 9, "bold")).pack(anchor=W)
        self.treeview_ex_goscie = ttk.Treeview(ramka_ex_kolumna_goscie,
                                               columns=("Imie", "Nazwisko", "Telefon", "Bilet"), show="headings",
                                               height=8)

        self.treeview_ex_goscie.heading("Imie", text="Imię");
        self.treeview_ex_goscie.heading("Nazwisko", text="Nazwisko");
        self.treeview_ex_goscie.heading("Telefon", text="Telefon");
        self.treeview_ex_goscie.heading("Bilet", text="Typ Biletu")
        for col in ("Imie", "Nazwisko", "Telefon", "Bilet"):
            self.treeview_ex_goscie.column(col, width=100, minwidth=50, stretch=True, anchor=CENTER)
        self.treeview_ex_goscie.pack(fill="both", expand=True, pady=2)


        # ZAKŁADKA 3: KADRY I GOŚCIE

        ramka_kadry_lewa = Frame(ramka_tab_kadry);
        ramka_kadry_lewa.pack(side=LEFT, padx=15, pady=10, fill=Y)

        ramka_e_formularz = LabelFrame(ramka_kadry_lewa, text=" Zarządzaj Pracownikiem ", padx=10, pady=5)
        ramka_e_formularz.pack(fill=X, pady=2)
        Label(ramka_e_formularz, text="Imię:").grid(row=0, column=0, sticky=W, pady=2)
        self.entry_e_imie = Entry(ramka_e_formularz, width=25);
        self.entry_e_imie.grid(row=0, column=1, pady=2)
        Label(ramka_e_formularz, text="Nazwisko:").grid(row=1, column=0, sticky=W, pady=2)
        self.entry_e_nazwisko = Entry(ramka_e_formularz, width=25);
        self.entry_e_nazwisko.grid(row=1, column=1, pady=2)
        Label(ramka_e_formularz, text="Nr tel:").grid(row=2, column=0, sticky=W, pady=2)
        self.entry_e_tel = Entry(ramka_e_formularz, width=25);
        self.entry_e_tel.grid(row=2, column=1, pady=2)
        Label(ramka_e_formularz, text="Stanowisko:").grid(row=3, column=0, sticky=W, pady=2)
        self.combobox_e_stanowisko = ttk.Combobox(ramka_e_formularz,
                                                  values=["Kustosz", "Kurator", "Przewodnik", "Edukator",
                                                          "Konserwator"], width=22, state="readonly")
        self.combobox_e_stanowisko.grid(row=3, column=1, pady=2);
        self.combobox_e_stanowisko.current(0)
        Label(ramka_e_formularz, text="Msc zamieszkania:").grid(row=4, column=0, sticky=W, pady=2)
        self.entry_e_dom = Entry(ramka_e_formularz, width=25);
        self.entry_e_dom.grid(row=4, column=1, pady=2)
        Label(ramka_e_formularz, text="Typ miejsca pr.:").grid(row=5, column=0, sticky=W, pady=2)
        self.combobox_e_typ = ttk.Combobox(ramka_e_formularz, values=["Galeria", "Wystawa"], width=22, state="readonly")
        self.combobox_e_typ.grid(row=5, column=1, pady=2);
        self.combobox_e_typ.current(0)
        Label(ramka_e_formularz, text="Wybierz obiekt:").grid(row=6, column=0, sticky=W, pady=2)
        self.combobox_e_miejsce = ttk.Combobox(ramka_e_formularz, width=22, state="readonly")
        self.combobox_e_miejsce.grid(row=6, column=1, pady=2)
        self.combobox_e_typ.bind("<<ComboboxSelected>>", lambda e: self.gui_refresh_dropdowns())
        self.button_e_akcja = Button(ramka_e_formularz, text="Zatrudnij", command=self.gui_add_employee, bg="#cce5ff")
        self.button_e_akcja.grid(row=7, column=0, columnspan=2, pady=6)

        ramka_guest_formularz = LabelFrame(ramka_kadry_lewa, text=" Rejestracja Wizyty ", padx=10, pady=5)
        ramka_guest_formularz.pack(fill=X, pady=5)
        Label(ramka_guest_formularz, text="Imię:").grid(row=0, column=0, sticky=W, pady=2)
        self.entry_guest_imie = Entry(ramka_guest_formularz, width=25);
        self.entry_guest_imie.grid(row=0, column=1, pady=2)
        Label(ramka_guest_formularz, text="Nazwisko:").grid(row=1, column=0, sticky=W, pady=2)
        self.entry_guest_nazwisko = Entry(ramka_guest_formularz, width=25);
        self.entry_guest_nazwisko.grid(row=1, column=1, pady=2)
        Label(ramka_guest_formularz, text="Nr tel:").grid(row=2, column=0, sticky=W, pady=2)
        self.entry_guest_tel = Entry(ramka_guest_formularz, width=25);
        self.entry_guest_tel.grid(row=2, column=1, pady=2)
        Label(ramka_guest_formularz, text="Typ biletu:").grid(row=3, column=0, sticky=W, pady=2)
        self.combobox_guest_bilet = ttk.Combobox(ramka_guest_formularz, values=["Normalny", "Ulgowy", "Rodzinny"],
                                                 width=22, state="readonly")
        self.combobox_guest_bilet.grid(row=3, column=1, pady=2);
        self.combobox_guest_bilet.current(0)
        Label(ramka_guest_formularz, text="Cel wizyty:").grid(row=4, column=0, sticky=W, pady=2)
        self.combobox_guest_typ = ttk.Combobox(ramka_guest_formularz, values=["Galeria", "Wystawa"], width=22,
                                               state="readonly")
        self.combobox_guest_typ.grid(row=4, column=1, pady=2);
        self.combobox_guest_typ.current(0)
        Label(ramka_guest_formularz, text="Wybierz obiekt:").grid(row=5, column=0, sticky=W, pady=2)
        self.combobox_guest_miejsce = ttk.Combobox(ramka_guest_formularz, width=22, state="readonly")
        self.combobox_guest_miejsce.grid(row=5, column=1, pady=2)
        self.combobox_guest_typ.bind("<<ComboboxSelected>>", lambda e: self.gui_refresh_dropdowns())
        self.button_guest_akcja = Button(ramka_guest_formularz, text="Zapisz wejście", command=self.gui_add_guest,
                                         bg="#fff3cd")
        self.button_guest_akcja.grid(row=6, column=0, columnspan=2, pady=6)

        ramka_kadry_prawa = Frame(ramka_tab_kadry);
        ramka_kadry_prawa.pack(side=RIGHT, fill="both", expand=True, padx=15, pady=10)
        ramka_tabele_kadry_kontener = Frame(ramka_kadry_prawa);
        ramka_tabele_kadry_kontener.pack(fill=X, pady=2)
        ramka_tabele_kadry_kontener.columnconfigure(0, weight=1, uniform="g_k");
        ramka_tabele_kadry_kontener.columnconfigure(1, weight=1, uniform="g_k")

        # TABELA 5: BAZA PRACOWNIKÓW
        ramka_k_kolumna_pracownicy = Frame(ramka_tabele_kadry_kontener);
        ramka_k_kolumna_pracownicy.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        Label(ramka_k_kolumna_pracownicy, text="Baza Pracowników:", font=("Arial", 10, "bold")).pack(anchor=W)
        self.treeview_zarzadzanie_pracownikami = ttk.Treeview(ramka_k_kolumna_pracownicy,
                                                              columns=("Imie", "Nazwisko", "Miejsce"), show="headings",
                                                              height=6)

        self.treeview_zarzadzanie_pracownikami.heading("Imie", text="Imię");
        self.treeview_zarzadzanie_pracownikami.heading("Nazwisko", text="Nazwisko");
        self.treeview_zarzadzanie_pracownikami.heading("Miejsce", text="Miejsce Pracy")
        for col in ("Imie", "Nazwisko", "Miejsce"):
            self.treeview_zarzadzanie_pracownikami.column(col, width=100, minwidth=50, stretch=True, anchor=CENTER)
        self.treeview_zarzadzanie_pracownikami.pack(fill=BOTH, expand=True, pady=2)
        self.treeview_zarzadzanie_pracownikami.bind("<<TreeviewSelect>>", self.gui_on_employee_selected)

        ramka_k_akcje_pracownicy = Frame(ramka_k_kolumna_pracownicy);
        ramka_k_akcje_pracownicy.pack(fill=X, pady=(0, 5))
        Button(ramka_k_akcje_pracownicy, text="Edytuj", command=self.gui_edit_employee).pack(side=RIGHT, padx=2)
        Button(ramka_k_akcje_pracownicy, text="Zwolnij", command=self.gui_remove_employee, fg="red").pack(side=RIGHT,
                                                                                                          padx=2)

        # TABELA 6: LISTA GOŚCI
        ramka_k_kolumna_goscie = Frame(ramka_tabele_kadry_kontener);
        ramka_k_kolumna_goscie.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        Label(ramka_k_kolumna_goscie, text="Lista Gości:", font=("Arial", 10, "bold")).pack(anchor=W)
        self.treeview_zarzadzanie_goscmi = ttk.Treeview(ramka_k_kolumna_goscie, columns=("Imie", "Nazwisko", "Cel"),
                                                        show="headings", height=6)

        self.treeview_zarzadzanie_goscmi.heading("Imie", text="Imię");
        self.treeview_zarzadzanie_goscmi.heading("Nazwisko", text="Nazwisko");
        self.treeview_zarzadzanie_goscmi.heading("Cel", text="Cel wizyty")
        for col in ("Imie", "Nazwisko", "Cel"):
            self.treeview_zarzadzanie_goscmi.column(col, width=100, minwidth=50, stretch=True, anchor=CENTER)
        self.treeview_zarzadzanie_goscmi.pack(fill=BOTH, expand=True, pady=2)
        self.treeview_zarzadzanie_goscmi.bind("<<TreeviewSelect>>", self.gui_on_guest_selected)

        ramka_k_akcje_goscie = Frame(ramka_k_kolumna_goscie);
        ramka_k_akcje_goscie.pack(anchor=E, pady=(0, 5))
        Button(ramka_k_akcje_goscie, text="Edytuj", command=self.gui_edit_guest).pack(side=LEFT, padx=2)
        Button(ramka_k_akcje_goscie, text="Usuń", command=self.gui_remove_guest, fg="red").pack(side=LEFT, padx=2)

        self.label_szczegoly_kadry_wartosc = Label(ramka_kadry_prawa, text="Zaznacz obiekt, by wyświetlić dane.",
                                                   font=("Arial", 9, "italic"), anchor=W, justify=LEFT)
        self.label_szczegoly_kadry_wartosc.pack(fill=X, pady=2)

        self.map_widget_emp = tkintermapview.TkinterMapView(ramka_kadry_prawa, corner_radius=10, height=340)
        self.map_widget_emp.pack(fill="both", expand=True, pady=5)

        main_notebook.bind("<<NotebookTabChanged>>", lambda e: self.gui_refresh_dropdowns())


    # REAKCJE INTERFEJSU


    def gui_refresh_dropdowns(self):
        g_names = [g.nazwa for g in model.galleries]
        e_names = [ex.nazwa for ex in model.exhibitions]
        self.combobox_e_miejsce['values'] = g_names if self.combobox_e_typ.get() == "Galeria" else e_names
        self.combobox_guest_miejsce['values'] = g_names if self.combobox_guest_typ.get() == "Galeria" else e_names

    def rebuild_all_markers_on_startup(self):
        for g in model.galleries:
            self.markers[g] = self.map_widget_g.set_marker(g.coordinates[0], g.coordinates[1], text=g.nazwa)
        for ex in model.exhibitions:
            self.markers[ex] = self.map_widget_ex.set_marker(ex.coordinates[0], ex.coordinates[1], text=ex.nazwa)
        for emp in model.employees:
            self.markers[emp] = self.map_widget_emp.set_marker(emp.coordinates[0], emp.coordinates[1],
                                                               text=f"{emp.imie} {emp.nazwisko}")

    def refresh_all_views(self):
        self.listbox_galerie.delete(0, END)
        for idx, g in enumerate(model.galleries):
            self.listbox_galerie.insert(idx, f"{g.nazwa} ({g.lokalizacja})")

        self.listbox_wystawy.delete(0, END)
        for idx, ex in enumerate(model.exhibitions):
            self.listbox_wystawy.insert(idx, f"{ex.nazwa} ({ex.lokalizacja})")

        for row in self.treeview_zarzadzanie_pracownikami.get_children(): self.treeview_zarzadzanie_pracownikami.delete(
            row)
        for emp in model.employees:
            self.treeview_zarzadzanie_pracownikami.insert("", END, values=(emp.imie, emp.nazwisko,
                                                                           f"{emp.miejsce} ({emp.typ_miejsca})"))

        for row in self.treeview_zarzadzanie_goscmi.get_children(): self.treeview_zarzadzanie_goscmi.delete(row)
        for gst in model.guests:
            self.treeview_zarzadzanie_goscmi.insert("", END, values=(gst.imie, gst.nazwisko,
                                                                     f"{gst.miejsce} ({gst.typ_miejsca})"))

        self.gui_refresh_dropdowns()

    #  STRONA: GALERIE SZTUKI
    def gui_add_gallery(self):
        new_g = add_gallery(model.galleries, self.entry_g_nazwa.get(), self.entry_g_typ.get(), self.entry_g_lok.get())
        if new_g:
            self.markers[new_g] = self.map_widget_g.set_marker(new_g.coordinates[0], new_g.coordinates[1],
                                                               text=new_g.nazwa)
            self.map_widget_g.set_position(new_g.coordinates[0], new_g.coordinates[1])
            self.entry_g_nazwa.delete(0, END);
            self.entry_g_typ.delete(0, END);
            self.entry_g_lok.delete(0, END)
            self.refresh_all_views()

    def gui_remove_gallery(self):
        if not self.listbox_galerie.curselection(): return
        idx = self.listbox_galerie.index(ACTIVE)
        removed_obj = remove_gallery(model.galleries, idx)
        if removed_obj and removed_obj in self.markers:
            self.markers[removed_obj].delete()
            del self.markers[removed_obj]
        self.refresh_all_views()

    def gui_edit_gallery(self):
        if not self.listbox_galerie.curselection(): return
        idx = self.listbox_galerie.index(ACTIVE)
        g = model.galleries[idx]
        self.entry_g_nazwa.delete(0, END);
        self.entry_g_typ.delete(0, END);
        self.entry_g_lok.delete(0, END)
        self.entry_g_nazwa.insert(0, g.nazwa);
        self.entry_g_typ.insert(0, g.typ_sztuki);
        self.entry_g_lok.insert(0, g.lokalizacja)
        self.button_g_akcja.config(text="Zapisz zmiany", command=lambda: self.gui_update_gallery(idx), bg="#ffe8a1")

    def gui_update_gallery(self, idx):
        updated_g = update_gallery(model.galleries, idx, self.entry_g_nazwa.get(), self.entry_g_typ.get(),
                                   self.entry_g_lok.get())
        if updated_g:
            if updated_g in self.markers: self.markers[updated_g].delete()
            self.markers[updated_g] = self.map_widget_g.set_marker(updated_g.coordinates[0], updated_g.coordinates[1],
                                                                   text=updated_g.nazwa)
            self.map_widget_g.set_position(updated_g.coordinates[0], updated_g.coordinates[1])
            self.button_g_akcja.config(text="Dodaj galerię", command=self.gui_add_gallery, bg="#d4edda")
            self.entry_g_nazwa.delete(0, END);
            self.entry_g_typ.delete(0, END);
            self.entry_g_lok.delete(0, END)
            self.refresh_all_views()

    def gui_on_gallery_selected(self, event):
        if not self.listbox_galerie.curselection(): return
        g = model.galleries[self.listbox_galerie.index(ACTIVE)]
        self.map_widget_g.set_position(g.coordinates[0], g.coordinates[1])

    def gui_show_gallery_details(self):
        if not self.listbox_galerie.curselection(): return
        g = model.galleries[self.listbox_galerie.index(ACTIVE)]
        self.map_widget_g.set_position(g.coordinates[0], g.coordinates[1])
        self.map_widget_g.set_zoom(13)
        self.label_g_tytul_sekcji.config(text=f"Szczegóły dla: {g.nazwa} | Współrzędne: {g.coordinates}")

        for row in self.treeview_g_pracownicy.get_children(): self.treeview_g_pracownicy.delete(row)
        for row in self.treeview_g_goscie.get_children(): self.treeview_g_goscie.delete(row)

        for emp in model.employees:
            if emp.miejsce == g.nazwa and emp.typ_miejsca == "galeria":
                self.treeview_g_pracownicy.insert("", END,
                                                  values=(emp.imie, emp.nazwisko, emp.telefon, emp.stanowisko, emp.dom))
        for gst in model.guests:
            if gst.miejsce == g.nazwa and gst.typ_miejsca == "galeria":
                self.treeview_g_goscie.insert("", END, values=(gst.imie, gst.nazwisko, gst.telefon, gst.typ_bilet))

    #  STRONA: WYSTAWY
    def gui_add_exhibition(self):
        new_ex = add_exhibition(model.exhibitions, self.entry_ex_nazwa.get(), self.entry_ex_temat.get(),
                                self.entry_ex_lok.get())
        if new_ex:
            self.markers[new_ex] = self.map_widget_ex.set_marker(new_ex.coordinates[0], new_ex.coordinates[1],
                                                                 text=new_ex.nazwa)
            self.map_widget_ex.set_position(new_ex.coordinates[0], new_ex.coordinates[1])
            self.entry_ex_nazwa.delete(0, END);
            self.entry_ex_temat.delete(0, END);
            self.entry_ex_lok.delete(0, END)
            self.refresh_all_views()

    def gui_remove_exhibition(self):
        if not self.listbox_wystawy.curselection(): return
        idx = self.listbox_wystawy.index(ACTIVE)
        removed = remove_exhibition(model.exhibitions, idx)
        if removed and removed in self.markers: self.markers[removed].delete()
        self.refresh_all_views()

    def gui_edit_exhibition(self):
        if not self.listbox_wystawy.curselection(): return
        idx = self.listbox_wystawy.index(ACTIVE)
        ex = model.exhibitions[idx]
        self.entry_ex_nazwa.delete(0, END);
        self.entry_ex_temat.delete(0, END);
        self.entry_ex_lok.delete(0, END)
        self.entry_ex_nazwa.insert(0, ex.nazwa);
        self.entry_ex_temat.insert(0, ex.tematyka);
        self.entry_ex_lok.insert(0, ex.lokalizacja)
        self.button_ex_akcja.config(text="Zapisz zmiany", command=lambda: self.gui_update_exhibition(idx), bg="#ffe8a1")

    def gui_update_exhibition(self, idx):
        updated = update_exhibition(model.exhibitions, idx, self.entry_ex_nazwa.get(), self.entry_ex_temat.get(),
                                    self.entry_ex_lok.get())
        if updated:
            if updated in self.markers: self.markers[updated].delete()
            self.markers[updated] = self.map_widget_ex.set_marker(updated.coordinates[0], updated.coordinates[1],
                                                                  text=updated.nazwa)
            self.button_ex_akcja.config(text="Dodaj wystawę", command=self.gui_add_exhibition, bg="#d4edda")
            self.entry_ex_nazwa.delete(0, END);
            self.entry_ex_temat.delete(0, END);
            self.entry_ex_lok.delete(0, END)
            self.refresh_all_views()

    def gui_on_exhibition_selected(self, event):
        if not self.listbox_wystawy.curselection(): return
        ex = model.exhibitions[self.listbox_wystawy.index(ACTIVE)]
        self.map_widget_ex.set_position(ex.coordinates[0], ex.coordinates[1])

    def gui_show_exhibition_details(self):
        if not self.listbox_wystawy.curselection(): return
        ex = model.exhibitions[self.listbox_wystawy.index(ACTIVE)]
        self.map_widget_ex.set_position(ex.coordinates[0], ex.coordinates[1])
        self.map_widget_ex.set_zoom(13)
        self.label_ex_tytul_sekcji.config(text=f"Szczegóły dla: {ex.nazwa} | Współrzędne: {ex.coordinates}")

        for row in self.treeview_ex_pracownicy.get_children(): self.treeview_ex_pracownicy.delete(row)
        for row in self.treeview_ex_goscie.get_children(): self.treeview_ex_goscie.delete(row)

        for emp in model.employees:
            if emp.miejsce == ex.nazwa and emp.typ_miejsca == "wystawa":
                self.treeview_ex_pracownicy.insert("", END, values=(emp.imie, emp.nazwisko, emp.telefon, emp.stanowisko,
                                                                    emp.dom))
        for gst in model.guests:
            if gst.miejsce == ex.nazwa and gst.typ_miejsca == "wystawa":
                self.treeview_ex_goscie.insert("", END, values=(gst.imie, gst.nazwisko, gst.telefon, gst.typ_bilet))

    #  STRONA: KADRY
    def gui_add_employee(self):
        p_type = "galeria" if self.combobox_e_typ.get() == "Galeria" else "wystawa"
        new_emp = add_employee(model.employees, self.entry_e_imie.get(), self.entry_e_nazwisko.get(),
                               self.entry_e_tel.get(),
                               self.combobox_e_stanowisko.get(), self.combobox_e_miejsce.get(), p_type,
                               self.entry_e_dom.get())
        if new_emp:
            self.markers[new_emp] = self.map_widget_emp.set_marker(new_emp.coordinates[0], new_emp.coordinates[1],
                                                                   text=f"{new_emp.imie} {new_emp.nazwisko}")
            self.map_widget_emp.set_position(new_emp.coordinates[0], new_emp.coordinates[1])
            self.entry_e_imie.delete(0, END);
            self.entry_e_nazwisko.delete(0, END);
            self.entry_e_tel.delete(0, END);
            self.entry_e_dom.delete(0, END)
            self.refresh_all_views()

    def gui_remove_employee(self):
        selected = self.treeview_zarzadzanie_pracownikami.selection()
        if not selected: return
        idx = int(self.treeview_zarzadzanie_pracownikami.index(selected[0]))
        removed = remove_employee(model.employees, idx)
        if removed and removed in self.markers: self.markers[removed].delete()
        self.refresh_all_views()

    def gui_edit_employee(self):
        selected = self.treeview_zarzadzanie_pracownikami.selection()
        if not selected: return
        idx = int(self.treeview_zarzadzanie_pracownikami.index(selected[0]))
        emp = model.employees[idx]

        self.entry_e_imie.delete(0, END);
        self.entry_e_nazwisko.delete(0, END);
        self.entry_e_tel.delete(0, END);
        self.entry_e_dom.delete(0, END)
        self.entry_e_imie.insert(0, emp.imie);
        self.entry_e_nazwisko.insert(0, emp.nazwisko);
        self.entry_e_tel.insert(0, emp.telefon);
        self.entry_e_dom.insert(0, emp.dom)
        self.combobox_e_stanowisko.set(emp.stanowisko)
        self.combobox_e_typ.set("Galeria" if emp.typ_miejsca == "galeria" else "Wystawa")
        self.gui_refresh_dropdowns()
        self.combobox_e_miejsce.set(emp.miejsce)
        self.button_e_akcja.config(text="Zapisz zmiany", command=lambda: self.gui_update_employee(idx), bg="#ffe8a1")

    def gui_update_employee(self, idx):
        p_type = "galeria" if self.combobox_e_typ.get() == "Galeria" else "wystawa"
        updated = update_employee(model.employees, idx, self.entry_e_imie.get(), self.entry_e_nazwisko.get(),
                                  self.entry_e_tel.get(),
                                  self.combobox_e_stanowisko.get(), self.combobox_e_miejsce.get(), p_type,
                                  self.entry_e_dom.get())
        if updated:
            if updated in self.markers: self.markers[updated].delete()
            self.markers[updated] = self.map_widget_emp.set_marker(updated.coordinates[0], updated.coordinates[1],
                                                                   text=f"{updated.imie} {updated.nazwisko}")
            self.button_e_akcja.config(text="Zatrudnij", command=self.gui_add_employee, bg="#cce5ff")
            self.entry_e_imie.delete(0, END);
            self.entry_e_nazwisko.delete(0, END);
            self.entry_e_tel.delete(0, END);
            self.entry_e_dom.delete(0, END)
            self.refresh_all_views()

    def gui_on_employee_selected(self, event):
        selected = self.treeview_zarzadzanie_pracownikami.selection()
        if not selected: return
        idx = int(self.treeview_zarzadzanie_pracownikami.index(selected[0]))
        emp = model.employees[idx]
        self.map_widget_emp.set_position(emp.coordinates[0], emp.coordinates[1])
        self.map_widget_emp.set_zoom(13)
        self.label_szczegoly_kadry_wartosc.config(
            text=f"Pracownik: {emp.imie} {emp.nazwisko} | Stanowisko: {emp.stanowisko} | Dom: {emp.dom} {emp.coordinates}")

    #  STRONA: GOŚCIE
    def gui_add_guest(self):
        p_type = "galeria" if self.combobox_guest_typ.get() == "Galeria" else "wystawa"
        new_gst = add_guest(model.guests, self.entry_guest_imie.get(), self.entry_guest_nazwisko.get(),
                            self.entry_guest_tel.get(),
                            self.combobox_guest_bilet.get(), self.combobox_guest_miejsce.get(), p_type)
        if new_gst:
            self.entry_guest_imie.delete(0, END);
            self.entry_guest_nazwisko.delete(0, END);
            self.entry_guest_tel.delete(0, END)
            self.refresh_all_views()

    def gui_remove_guest(self):
        selected = self.treeview_zarzadzanie_goscmi.selection()
        if not selected: return
        idx = int(self.treeview_zarzadzanie_goscmi.index(selected[0]))
        remove_guest(model.guests, idx)
        self.refresh_all_views()

    def gui_edit_guest(self):
        selected = self.treeview_zarzadzanie_goscmi.selection()
        if not selected: return
        idx = int(self.treeview_zarzadzanie_goscmi.index(selected[0]))
        gst = model.guests[idx]

        self.entry_guest_imie.delete(0, END);
        self.entry_guest_nazwisko.delete(0, END);
        self.entry_guest_tel.delete(0, END)
        self.entry_guest_imie.insert(0, gst.imie);
        self.entry_guest_nazwisko.insert(0, gst.nazwisko);
        self.entry_guest_tel.insert(0, gst.telefon)
        self.combobox_guest_bilet.set(gst.typ_bilet)
        self.combobox_guest_typ.set("Galeria" if gst.typ_miejsca == "galeria" else "Wystawa")
        self.gui_refresh_dropdowns()
        self.combobox_guest_miejsce.set(gst.miejsce)
        self.button_guest_akcja.config(text="Zapisz zmiany", command=lambda: self.gui_update_guest(idx), bg="#ffe8a1")

    def gui_update_guest(self, idx):
        p_type = "galeria" if self.combobox_guest_typ.get() == "Galeria" else "wystawa"
        updated = update_guest(model.guests, idx, self.entry_guest_imie.get(), self.entry_guest_nazwisko.get(),
                               self.entry_guest_tel.get(),
                               self.combobox_guest_bilet.get(), self.combobox_guest_miejsce.get(), p_type)
        if updated:
            self.button_guest_akcja.config(text="Zapisz wejście", command=self.gui_add_guest, bg="#fff3cd")
            self.entry_guest_imie.delete(0, END);
            self.entry_guest_nazwisko.delete(0, END);
            self.entry_guest_tel.delete(0, END)
            self.refresh_all_views()

    def gui_on_guest_selected(self, event):
        selected = self.treeview_zarzadzanie_goscmi.selection()
        if not selected: return
        idx = int(self.treeview_zarzadzanie_goscmi.index(selected[0]))
        gst = model.guests[idx]
        self.label_szczegoly_kadry_wartosc.config(
            text=f"Gość: {gst.imie} {gst.nazwisko} | Bilet: {gst.typ_bilet} | Cel: {gst.miejsce} ({gst.typ_miejsca.upper()})")


if __name__ == "__main__":
    root = Tk()
    app = ApplicationWindow(root)
    root.mainloop()