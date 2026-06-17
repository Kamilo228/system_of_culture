from tkinter import *
from tkinter import ttk
import tkintermapview

import gallery_lib.model as model
from gallery_lib.controller import AppController

class ApplicationWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("System Kultury")
        self.root.geometry("1024x760")

        self.markers = {}
        self.controller = AppController(self)  

        self.build_gui()
        self.center_maps()

        self.controller.refresh_all_views()

    def center_maps(self):
        for m in (self.map_g, self.map_ex, self.map_emp):
            m.set_position(52.1130, 19.4236)
            m.set_zoom(6)

    def build_gui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tab_g = Frame(notebook)
        tab_ex = Frame(notebook)
        tab_emp = Frame(notebook)

        notebook.add(tab_g, text='   Galerie Sztuki   ')
        notebook.add(tab_ex, text='   Wystawy   ')
        notebook.add(tab_emp, text=' Panel Zarządzania  ')

        # --- ZAKŁADKA GALERII ---
        g_gora = Frame(tab_g)
        g_gora.pack(side=TOP, fill=X, padx=15, pady=5)
        g_lewa = Frame(g_gora)
        g_lewa.pack(side=LEFT, fill=Y)

        f_galeria = LabelFrame(g_lewa, text=" Formularz Galerii ", padx=10, pady=10)
        f_galeria.pack(fill=X, pady=5)
        Label(f_galeria, text="Nazwa:").grid(row=0, column=0, sticky=W, pady=2)
        self.ent_g_nazwa = Entry(f_galeria, width=28)
        self.ent_g_nazwa.grid(row=0, column=1, pady=2)
        Label(f_galeria, text="Typ sztuki:").grid(row=1, column=0, sticky=W, pady=2)
        self.ent_g_typ = Entry(f_galeria, width=28)
        self.ent_g_typ.grid(row=1, column=1, pady=2)
        Label(f_galeria, text="Miasto:").grid(row=2, column=0, sticky=W, pady=2)
        self.ent_g_lok = Entry(f_galeria, width=28)
        self.ent_g_lok.grid(row=2, column=1, pady=2)

        self.btn_g_akcja = Button(f_galeria, text="Dodaj galerię",
                                  command=lambda: self.controller.add_gallery(self.ent_g_nazwa.get(),
                                                                              self.ent_g_typ.get(),
                                                                              self.ent_g_lok.get()), bg="#d4edda")
        self.btn_g_akcja.grid(row=3, column=0, columnspan=2, pady=8)

        szukaj_g = Frame(g_lewa)
        szukaj_g.pack(fill=X, pady=(5, 0))
        Label(szukaj_g, text="Szukaj:").pack(side=LEFT)
        self.ent_szukaj_g = Entry(szukaj_g)
        self.ent_szukaj_g.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.ent_szukaj_g.bind("<KeyRelease>", lambda e: self.controller.search_gallery_changed())

        Label(g_lewa, text="Lista Galerii:").pack(anchor=W, pady=(5, 2))
        self.list_g = Listbox(g_lewa, width=44, height=11)
        self.list_g.pack(fill=X)
        self.list_g.bind("<<ListboxSelect>>", lambda e: self.controller.gallery_selected(self.list_g.index(ACTIVE)))

        g_przyciski = Frame(g_lewa)
        g_przyciski.pack(fill=X, pady=5)
        self.btn_g_szczegoly = Button(g_przyciski, text="Pokaż szczegóły",
                                      command=lambda: self.controller.toggle_gallery_details(self.list_g.index(ACTIVE),
                                                                                             bool(
                                                                                                 self.list_g.curselection())),
                                      bg="#cce5ff")
        self.btn_g_szczegoly.pack(fill=X, pady=2)
        Button(g_przyciski, text="Edytuj",
               command=lambda: self.controller.edit_gallery_clicked(self.list_g.index(ACTIVE),
                                                                    bool(self.list_g.curselection()))).pack(side=LEFT,
                                                                                                            expand=True,
                                                                                                            fill=X,
                                                                                                            padx=2,
                                                                                                            pady=2)
        Button(g_przyciski, text="Usuń", command=lambda: self.controller.remove_gallery(self.list_g.index(ACTIVE), bool(
            self.list_g.curselection())), fg="red").pack(side=LEFT, expand=True, fill=X, padx=2, pady=2)

        g_prawa = Frame(g_gora)
        g_prawa.pack(side=RIGHT, fill="both", expand=True, padx=(15, 0))
        self.map_g = tkintermapview.TkinterMapView(g_prawa, corner_radius=10, height=330)
        self.map_g.pack(fill="both", expand=True, pady=5)

        g_dol = Frame(tab_g)
        g_dol.pack(side=BOTTOM, fill="both", expand=True, padx=15, pady=5)
        self.lbl_g_sekcja = Label(g_dol, text="Szczegóły obiektu: (Wybierz galerię i kliknij 'Pokaż szczegóły')",
                                  font=("Arial", 10, "italic", "bold"), fg="#333333")
        self.lbl_g_sekcja.pack(anchor=W, pady=(0, 5))

        g_siatka = Frame(g_dol)
        g_siatka.pack(fill="both", expand=True)
        g_siatka.columnconfigure(0, weight=1, uniform="g")
        g_siatka.columnconfigure(1, weight=1, uniform="g")

        g_kol_pracownicy = Frame(g_siatka)
        g_kol_pracownicy.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        Label(g_kol_pracownicy, text="Pracownicy:", font=("Arial", 9, "bold")).pack(anchor=W)
        self.tree_g_emp = ttk.Treeview(g_kol_pracownicy, columns=("Imie", "Nazwisko", "Telefon", "Stanowisko", "Dom"),
                                       show="headings", height=8)
        for col in ("Imie", "Nazwisko", "Telefon", "Stanowisko", "Dom"):
            self.tree_g_emp.heading(col, text=col)
            self.tree_g_emp.column(col, width=100, anchor=CENTER)
        self.tree_g_emp.pack(fill="both", expand=True, pady=2)

        g_kol_goscie = Frame(g_siatka)
        g_kol_goscie.grid(row=0, column=1, sticky="nsew")
        Label(g_kol_goscie, text="Goście:", font=("Arial", 9, "bold")).pack(anchor=W)
        self.tree_g_gst = ttk.Treeview(g_kol_goscie, columns=("Imie", "Nazwisko", "Telefon", "Bilet"), show="headings",
                                       height=8)
        for col in ("Imie", "Nazwisko", "Telefon", "Bilet"):
            self.tree_g_gst.heading(col, text=col)
            self.tree_g_gst.column(col, width=100, anchor=CENTER)
        self.tree_g_gst.pack(fill="both", expand=True, pady=2)

        # --- ZAKŁADKA WYSTAW ---
        ex_gora = Frame(tab_ex)
        ex_gora.pack(side=TOP, fill=X, padx=15, pady=5)
        ex_lewa = Frame(ex_gora)
        ex_lewa.pack(side=LEFT, fill=Y)

        f_wystawa = LabelFrame(ex_lewa, text=" Formularz Wystawy ", padx=10, pady=10)
        f_wystawa.pack(fill=X, pady=5)
        Label(f_wystawa, text="Nazwa:").grid(row=0, column=0, sticky=W, pady=2)
        self.ent_ex_nazwa = Entry(f_wystawa, width=28)
        self.ent_ex_nazwa.grid(row=0, column=1, pady=2)
        Label(f_wystawa, text="Tematyka:").grid(row=1, column=0, sticky=W, pady=2)
        self.ent_ex_temat = Entry(f_wystawa, width=28)
        self.ent_ex_temat.grid(row=1, column=1, pady=2)
        Label(f_wystawa, text="Miasto:").grid(row=2, column=0, sticky=W, pady=2)
        self.ent_ex_lok = Entry(f_wystawa, width=28)
        self.ent_ex_lok.grid(row=2, column=1, pady=2)
        self.btn_ex_akcja = Button(f_wystawa, text="Dodaj wystawę",
                                   command=lambda: self.controller.add_exhibition(self.ent_ex_nazwa.get(),
                                                                                  self.ent_ex_temat.get(),
                                                                                  self.ent_ex_lok.get()), bg="#d4edda")
        self.btn_ex_akcja.grid(row=3, column=0, columnspan=2, pady=8)

        szukaj_ex = Frame(ex_lewa)
        szukaj_ex.pack(fill=X, pady=(5, 0))
        Label(szukaj_ex, text="Szukaj:").pack(side=LEFT)
        self.ent_szukaj_ex = Entry(szukaj_ex)
        self.ent_szukaj_ex.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.ent_szukaj_ex.bind("<KeyRelease>", lambda e: self.controller.search_exhibition_changed())

        Label(ex_lewa, text="Lista Wystaw:").pack(anchor=W, pady=(5, 2))
        self.list_ex = Listbox(ex_lewa, width=44, height=11)
        self.list_ex.pack(fill=X)
        self.list_ex.bind("<<ListboxSelect>>",
                          lambda e: self.controller.exhibition_selected(self.list_ex.index(ACTIVE)))

        ex_przyciski = Frame(ex_lewa)
        ex_przyciski.pack(fill=X, pady=5)
        self.btn_ex_szczegoly = Button(ex_przyciski, text="Pokaż szczegóły",
                                       command=lambda: self.controller.toggle_exhibition_details(
                                           self.list_ex.index(ACTIVE), bool(self.list_ex.curselection())), bg="#cce5ff")
        self.btn_ex_szczegoly.pack(fill=X, pady=2)
        Button(ex_przyciski, text="Edytuj",
               command=lambda: self.controller.edit_exhibition_clicked(self.list_ex.index(ACTIVE),
                                                                       bool(self.list_ex.curselection()))).pack(
            side=LEFT, expand=True, fill=X, padx=2, pady=2)
        Button(ex_przyciski, text="Usuń", command=lambda: self.controller.remove_exhibition(self.list_ex.index(ACTIVE),
                                                                                            bool(
                                                                                                self.list_ex.curselection())),
               fg="red").pack(side=LEFT, expand=True, fill=X, padx=2, pady=2)

        ex_prawa = Frame(ex_gora)
        ex_prawa.pack(side=RIGHT, fill="both", expand=True, padx=(15, 0))
        self.map_ex = tkintermapview.TkinterMapView(ex_prawa, corner_radius=10, height=330)
        self.map_ex.pack(fill="both", expand=True, pady=5)

        ex_dol = Frame(tab_ex)
        ex_dol.pack(side=BOTTOM, fill="both", expand=True, padx=15, pady=5)
        self.lbl_ex_sekcja = Label(ex_dol, text="Szczegóły obiektu: (Wybierz wystawę i kliknij 'Pokaż szczegóły')",
                                   font=("Arial", 10, "italic", "bold"), fg="#333333")
        self.lbl_ex_sekcja.pack(anchor=W, pady=(0, 5))

        ex_siatka = Frame(ex_dol)
        ex_siatka.pack(fill="both", expand=True)
        ex_siatka.columnconfigure(0, weight=1, uniform="ex")
        ex_siatka.columnconfigure(1, weight=1, uniform="ex")

        ex_kol_pracownicy = Frame(ex_siatka)
        ex_kol_pracownicy.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        Label(ex_kol_pracownicy, text="Pracownicy:", font=("Arial", 9, "bold")).pack(anchor=W)
        self.tree_ex_emp = ttk.Treeview(ex_kol_pracownicy, columns=("Imie", "Nazwisko", "Telefon", "Stanowisko", "Dom"),
                                        show="headings", height=8)
        for col in ("Imie", "Nazwisko", "Telefon", "Stanowisko", "Dom"):
            self.tree_ex_emp.heading(col, text=col)
            self.tree_ex_emp.column(col, width=100, anchor=CENTER)
        self.tree_ex_emp.pack(fill="both", expand=True, pady=2)

        ex_kol_goscie = Frame(ex_siatka)
        ex_kol_goscie.grid(row=0, column=1, sticky="nsew")
        Label(ex_kol_goscie, text="Goście:", font=("Arial", 9, "bold")).pack(anchor=W)
        self.tree_ex_gst = ttk.Treeview(ex_kol_goscie, columns=("Imie", "Nazwisko", "Telefon", "Bilet"),
                                        show="headings", height=8)
        for col in ("Imie", "Nazwisko", "Telefon", "Bilet"):
            self.tree_ex_gst.heading(col, text=col)
            self.tree_ex_gst.column(col, width=100, anchor=CENTER)
        self.tree_ex_gst.pack(fill="both", expand=True, pady=2)

        # --- PANEL ZARZĄDZANIA (KADRY/GOŚCIE) ---
        emp_lewa = Frame(tab_emp)
        emp_lewa.pack(side=LEFT, padx=15, pady=10, fill=Y)

        f_pracownik = LabelFrame(emp_lewa, text=" Pracownik ", padx=10, pady=5)
        f_pracownik.pack(fill=X, pady=2)
        Label(f_pracownik, text="Imię:").grid(row=0, column=0, sticky=W, pady=2)
        self.ent_e_imie = Entry(f_pracownik, width=25)
        self.ent_e_imie.grid(row=0, column=1, pady=2)
        Label(f_pracownik, text="Nazwisko:").grid(row=1, column=0, sticky=W, pady=2)
        self.ent_e_nazwisko = Entry(f_pracownik, width=25)
        self.ent_e_nazwisko.grid(row=1, column=1, pady=2)
        Label(f_pracownik, text="Tel:").grid(row=2, column=0, sticky=W, pady=2)
        self.ent_e_tel = Entry(f_pracownik, width=25)
        self.ent_e_tel.grid(row=2, column=1, pady=2)
        Label(f_pracownik, text="Stanowisko:").grid(row=3, column=0, sticky=W, pady=2)
        self.cmb_e_stanowisko = ttk.Combobox(f_pracownik,
                                             values=["Kustosz", "Kurator", "Przewodnik", "Edukator", "Konserwator"],
                                             width=22, state="readonly")
        self.cmb_e_stanowisko.grid(row=3, column=1, pady=2)
        self.cmb_e_stanowisko.current(0)
        Label(f_pracownik, text="Dom:").grid(row=4, column=0, sticky=W, pady=2)
        self.ent_e_dom = Entry(f_pracownik, width=25)
        self.ent_e_dom.grid(row=4, column=1, pady=2)
        Label(f_pracownik, text="Typ miejsca:").grid(row=5, column=0, sticky=W, pady=2)
        self.cmb_e_typ = ttk.Combobox(f_pracownik, values=["Galeria", "Wystawa"], width=22, state="readonly")
        self.cmb_e_typ.grid(row=5, column=1, pady=2)
        self.cmb_e_typ.current(0)
        Label(f_pracownik, text="Obiekt:").grid(row=6, column=0, sticky=W, pady=2)
        self.cmb_e_miejsce = ttk.Combobox(f_pracownik, width=22, state="readonly")
        self.cmb_e_miejsce.grid(row=6, column=1, pady=2)
        self.cmb_e_typ.bind("<<ComboboxSelected>>", lambda e: self.controller.refresh_all_views())

        self.btn_e_akcja = Button(f_pracownik, text="Zatrudnij",
                                  command=lambda: self.controller.add_employee(self.ent_e_imie.get(),
                                                                               self.ent_e_nazwisko.get(),
                                                                               self.ent_e_tel.get(),
                                                                               self.cmb_e_stanowisko.get(),
                                                                               self.cmb_e_miejsce.get(),
                                                                               self.cmb_e_typ.get().lower(),
                                                                               self.ent_e_dom.get()), bg="#cce5ff")
        self.btn_e_akcja.grid(row=7, column=0, columnspan=2, pady=6)

        f_gosc = LabelFrame(emp_lewa, text=" Wizyta Gościa ", padx=10, pady=5)
        f_gosc.pack(fill=X, pady=5)
        Label(f_gosc, text="Imię:").grid(row=0, column=0, sticky=W, pady=2)
        self.ent_gst_imie = Entry(f_gosc, width=25)
        self.ent_gst_imie.grid(row=0, column=1, pady=2)
        Label(f_gosc, text="Nazwisko:").grid(row=1, column=0, sticky=W, pady=2)
        self.ent_gst_nazwisko = Entry(f_gosc, width=25)
        self.ent_gst_nazwisko.grid(row=1, column=1, pady=2)
        Label(f_gosc, text="Tel:").grid(row=2, column=0, sticky=W, pady=2)
        self.ent_gst_tel = Entry(f_gosc, width=25)
        self.ent_gst_tel.grid(row=2, column=1, pady=2)
        Label(f_gosc, text="Bilet:").grid(row=3, column=0, sticky=W, pady=2)
        self.cmb_gst_bilet = ttk.Combobox(f_gosc, values=["Normalny", "Ulgowy", "Rodzinny"], width=22, state="readonly")
        self.cmb_gst_bilet.grid(row=3, column=1, pady=2)
        self.cmb_gst_bilet.current(0)
        Label(f_gosc, text="Cel:").grid(row=4, column=0, sticky=W, pady=2)
        self.cmb_gst_typ = ttk.Combobox(f_gosc, values=["Galeria", "Wystawa"], width=22, state="readonly")
        self.cmb_gst_typ.grid(row=4, column=1, pady=2)
        self.cmb_gst_typ.current(0)
        Label(f_gosc, text="Obiekt:").grid(row=5, column=0, sticky=W, pady=2)
        self.cmb_gst_miejsce = ttk.Combobox(f_gosc, width=22, state="readonly")
        self.cmb_gst_miejsce.grid(row=5, column=1, pady=2)
        self.cmb_gst_typ.bind("<<ComboboxSelected>>", lambda e: self.controller.refresh_all_views())

        self.btn_gst_akcja = Button(f_gosc, text="Zapisz wejście",
                                    command=lambda: self.controller.add_guest(self.ent_gst_imie.get(),
                                                                              self.ent_gst_nazwisko.get(),
                                                                              self.ent_gst_tel.get(),
                                                                              self.cmb_gst_bilet.get(),
                                                                              self.cmb_gst_miejsce.get(),
                                                                              self.cmb_gst_typ.get().lower()),
                                    bg="#fff3cd")
        self.btn_gst_akcja.grid(row=6, column=0, columnspan=2, pady=6)

        emp_prawa = Frame(tab_emp)
        emp_prawa.pack(side=RIGHT, fill="both", expand=True, padx=15, pady=10)
        emp_tabele = Frame(emp_prawa)
        emp_tabele.pack(fill=X, pady=2)
        emp_tabele.columnconfigure(0, weight=1, uniform="mgr")
        emp_tabele.columnconfigure(1, weight=1, uniform="mgr")

        kol_baza_emp = Frame(emp_tabele)
        kol_baza_emp.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        Label(kol_baza_emp, text="Baza Pracowników:", font=("Arial", 10, "bold")).pack(anchor=W)
        self.tree_mgr_emp = ttk.Treeview(kol_baza_emp, columns=("Imie", "Nazwisko", "Miejsce"), show="headings",
                                         height=6)
        for col in ("Imie", "Nazwisko", "Miejsce"):
            self.tree_mgr_emp.heading(col, text=col)
            self.tree_mgr_emp.column(col, width=100, anchor=CENTER)
        self.tree_mgr_emp.pack(fill=BOTH, expand=True, pady=2)
        self.tree_mgr_emp.bind("<<TreeviewSelect>>",
                               lambda e: self.controller.employee_selected(self.get_tree_idx(self.tree_mgr_emp)))

        akcje_emp = Frame(kol_baza_emp)
        akcje_emp.pack(fill=X, pady=(0, 5))
        Button(akcje_emp, text="Edytuj", command=self.bridge_edit_emp).pack(side=RIGHT, padx=2)
        Button(akcje_emp, text="Zwolnij",
               command=lambda: self.controller.remove_employee(self.get_tree_idx(self.tree_mgr_emp)), fg="red").pack(
            side=RIGHT, padx=2)

        kol_baza_gst = Frame(emp_tabele)
        kol_baza_gst.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        Label(kol_baza_gst, text="Lista Gości:", font=("Arial", 10, "bold")).pack(anchor=W)
        self.tree_mgr_gst = ttk.Treeview(kol_baza_gst, columns=("Imie", "Nazwisko", "Cel"), show="headings", height=6)
        for col in ("Imie", "Nazwisko", "Cel"):
            self.tree_mgr_gst.heading(col, text=col)
            self.tree_mgr_gst.column(col, width=100, anchor=CENTER)
        self.tree_mgr_gst.pack(fill=BOTH, expand=True, pady=2)
        self.tree_mgr_gst.bind("<<TreeviewSelect>>",
                               lambda e: self.controller.guest_selected(self.get_tree_idx(self.tree_mgr_gst)))

        akcje_gst = Frame(kol_baza_gst)
        akcje_gst.pack(anchor=E, pady=(0, 5))
        Button(akcje_gst, text="Edytuj", command=self.bridge_edit_gst).pack(side=LEFT, padx=2)
        Button(akcje_gst, text="Usuń",
               command=lambda: self.controller.remove_guest(self.get_tree_idx(self.tree_mgr_gst)), fg="red").pack(
            side=LEFT, padx=2)

        self.lbl_mgr_szczegoly = Label(emp_prawa, text="Zaznacz obiekt, by wyświetlić dane.",
                                       font=("Arial", 9, "italic"), anchor=W, justify=LEFT)
        self.lbl_mgr_szczegoly.pack(fill=X, pady=2)

        self.map_emp = tkintermapview.TkinterMapView(emp_prawa, corner_radius=10, height=340)
        self.map_emp.pack(fill="both", expand=True, pady=5)

        notebook.bind("<<NotebookTabChanged>>", lambda e: self.controller.refresh_all_views())

    # --- POMOCNICZE GETTERY ---
    def get_search_gallery_text(self):
        return self.ent_szukaj_g.get()

    def get_search_exhibition_text(self):
        return self.ent_szukaj_ex.get()

    def get_tree_idx(self, tree):
        sel = tree.selection()
        return int(tree.index(sel[0])) if sel else None

    # --- METODY AKTUALIZACJI WIDOKU (DLA KONTROLERA) ---
    def update_gallery_listbox(self, items, all_galleries):
        self.list_g.delete(0, END)
        for i, text in enumerate(items): self.list_g.insert(i, text)

        self.map_g.delete_all_marker()
        self.markers = {k: v for k, v in self.markers.items() if type(k) != model.Gallery}
        for g in all_galleries:
            self.markers[g] = self.map_g.set_marker(g.coordinates[0], g.coordinates[1], text=g.nazwa)

    def update_exhibition_listbox(self, items, all_exhibitions):
        self.list_ex.delete(0, END)
        for i, text in enumerate(items): self.list_ex.insert(i, text)

        self.map_ex.delete_all_marker()
        self.markers = {k: v for k, v in self.markers.items() if type(k) != model.Exhibition}
        for ex in all_exhibitions:
            self.markers[ex] = self.map_ex.set_marker(ex.coordinates[0], ex.coordinates[1], text=ex.nazwa)

    def update_management_trees(self, emps, gsts):
        for r in self.tree_mgr_emp.get_children(): self.tree_mgr_emp.delete(r)
        for emp in emps: self.tree_mgr_emp.insert("", END,
                                                  values=(emp.imie, emp.nazwisko, f"{emp.miejsce} ({emp.typ_miejsca})"))
        for r in self.tree_mgr_gst.get_children(): self.tree_mgr_gst.delete(r)
        for gst in gsts: self.tree_mgr_gst.insert("", END,
                                                  values=(gst.imie, gst.nazwisko, f"{gst.miejsce} ({gst.typ_miejsca})"))

        self.map_emp.delete_all_marker()
        self.markers = {k: v for k, v in self.markers.items() if type(k) != model.Employee}
        for emp in emps:
            self.markers[emp] = self.map_emp.set_marker(emp.coordinates[0], emp.coordinates[1],
                                                        text=f"{emp.imie} {emp.nazwisko}")

    def refresh_dropdown_options(self, g_names, e_names):
        self.cmb_e_miejsce['values'] = g_names if self.cmb_e_typ.get() == "Galeria" else e_names
        self.cmb_gst_miejsce['values'] = g_names if self.cmb_gst_typ.get() == "Galeria" else e_names

    def move_map_to(self, target, coords):
        m = self.map_g if target == "galeria" else (self.map_ex if target == "wystawa" else self.map_emp)
        m.set_position(coords[0], coords[1])
        if target != "wystawa" and target != "galeria": m.set_zoom(13)

    # --- WIDOKI SZCZEGÓŁOWE ---
    def show_gallery_details_view(self, g, emps, gsts):
        self.btn_g_szczegoly.config(text="Pokaż wszystkie", bg="#ffcccc")
        self.list_g.delete(0, END)
        self.list_g.insert(0, f"{g.nazwa} ({g.lokalizacja})")
        self.map_g.delete_all_marker()
        self.markers = {k: v for k, v in self.markers.items() if type(k) != model.Gallery}
        self.markers[g] = self.map_g.set_marker(g.coordinates[0], g.coordinates[1], text=g.nazwa)
        self.map_g.set_position(g.coordinates[0], g.coordinates[1])
        self.map_g.set_zoom(14)
        self.lbl_g_sekcja.config(text=f"Szczegóły dla: {g.nazwa} | Współrzędne: {g.coordinates}")

        for row in self.tree_g_emp.get_children(): self.tree_g_emp.delete(row)
        for emp in emps: self.tree_g_emp.insert("", END,
                                                values=(emp.imie, emp.nazwisko, emp.telefon, emp.stanowisko, emp.dom))
        for row in self.tree_g_gst.get_children(): self.tree_g_gst.delete(row)
        for gst in gsts: self.tree_g_gst.insert("", END, values=(gst.imie, gst.nazwisko, gst.telefon, gst.typ_bilet))

    def clear_gallery_details_view(self):
        self.btn_g_szczegoly.config(text="Pokaż szczegóły", bg="#cce5ff")
        self.lbl_g_sekcja.config(text="Szczegóły obiektu: (Wybierz galerię i kliknij 'Pokaż szczegóły')")
        for row in self.tree_g_emp.get_children(): self.tree_g_emp.delete(row)
        for row in self.tree_g_gst.get_children(): self.tree_g_gst.delete(row)
        self.center_maps()

    def show_exhibition_details_view(self, ex, emps, gsts):
        self.btn_ex_szczegoly.config(text="Pokaż wszystkie", bg="#ffcccc")
        self.list_ex.delete(0, END)
        self.list_ex.insert(0, f"{ex.nazwa} ({ex.lokalizacja})")
        self.map_ex.delete_all_marker()
        self.markers = {k: v for k, v in self.markers.items() if type(k) != model.Exhibition}
        self.markers[ex] = self.map_ex.set_marker(ex.coordinates[0], ex.coordinates[1], text=ex.nazwa)
        self.map_ex.set_position(ex.coordinates[0], ex.coordinates[1])
        self.map_ex.set_zoom(14)
        self.lbl_ex_sekcja.config(text=f"Szczegóły dla: {ex.nazwa} | Współrzędne: {ex.coordinates}")

        for row in self.tree_ex_emp.get_children(): self.tree_ex_emp.delete(row)
        for emp in emps: self.tree_ex_emp.insert("", END,
                                                 values=(emp.imie, emp.nazwisko, emp.telefon, emp.stanowisko, emp.dom))
        for row in self.tree_ex_gst.get_children(): self.tree_ex_gst.delete(row)
        for gst in gsts: self.tree_ex_gst.insert("", END, values=(gst.imie, gst.nazwisko, gst.telefon, gst.typ_bilet))

    def clear_exhibition_details_view(self):
        self.btn_ex_szczegoly.config(text="Pokaż szczegóły", bg="#cce5ff")
        self.lbl_ex_sekcja.config(text="Szczegóły obiektu: (Wybierz wystawę i kliknij 'Pokaż szczegóły')")
        for row in self.tree_ex_emp.get_children(): self.tree_ex_emp.delete(row)
        for row in self.tree_ex_gst.get_children(): self.tree_ex_gst.delete(row)
        self.center_maps()

    def reset_gallery_details_button(self):
        self.btn_g_szczegoly.config(text="Pokaż szczegóły", bg="#cce5ff")

    def reset_exhibition_details_button(self):
        self.btn_ex_szczegoly.config(text="Pokaż szczegóły", bg="#cce5ff")

    def set_management_details_text(self, text):
        self.lbl_mgr_szczegoly.config(text=text)

    # --- CZYSZCZENIE I WYPEŁNIANIE INPUTÓW ---
    def clear_gallery_inputs(self):
        for ent in (self.ent_g_nazwa, self.ent_g_typ, self.ent_g_lok): ent.delete(0, END)
        self.btn_g_akcja.config(text="Dodaj galerię",
                                command=lambda: self.controller.add_gallery(self.ent_g_nazwa.get(),
                                                                            self.ent_g_typ.get(), self.ent_g_lok.get()),
                                bg="#d4edda")

    def populate_gallery_inputs(self, g, real_idx):
        self.clear_gallery_inputs()
        self.ent_g_nazwa.insert(0, g.nazwa)
        self.ent_g_typ.insert(0, g.typ_sztuki)
        self.ent_g_lok.insert(0, g.lokalizacja)
        self.btn_g_akcja.config(text="Zapisz zmiany",
                                command=lambda: self.controller.save_gallery_update(real_idx, self.ent_g_nazwa.get(),
                                                                                    self.ent_g_typ.get(),
                                                                                    self.ent_g_lok.get()), bg="#ffe8a1")

    def clear_exhibition_inputs(self):
        for ent in (self.ent_ex_nazwa, self.ent_ex_temat, self.ent_ex_lok): ent.delete(0, END)
        self.btn_ex_akcja.config(text="Dodaj wystawę",
                                 command=lambda: self.controller.add_exhibition(self.ent_ex_nazwa.get(),
                                                                                self.ent_ex_temat.get(),
                                                                                self.ent_ex_lok.get()), bg="#d4edda")

    def populate_exhibition_inputs(self, ex, real_idx):
        self.clear_exhibition_inputs()
        self.ent_ex_nazwa.insert(0, ex.nazwa)
        self.ent_ex_temat.insert(0, ex.tematyka)
        self.ent_ex_lok.insert(0, ex.lokalizacja)
        self.btn_ex_akcja.config(text="Zapisz zmiany", command=lambda: self.controller.save_exhibition_update(real_idx,
                                                                                                              self.ent_ex_nazwa.get(),
                                                                                                              self.ent_ex_temat.get(),
                                                                                                              self.ent_ex_lok.get()),
                                 bg="#ffe8a1")

    def clear_employee_inputs(self):
        for ent in (self.ent_e_imie, self.ent_e_nazwisko, self.ent_e_tel, self.ent_e_dom): ent.delete(0, END)
        self.btn_e_akcja.config(text="Zatrudnij", command=lambda: self.controller.add_employee(self.ent_e_imie.get(),
                                                                                               self.ent_e_nazwisko.get(),
                                                                                               self.ent_e_tel.get(),
                                                                                               self.cmb_e_stanowisko.get(),
                                                                                               self.cmb_e_miejsce.get(),
                                                                                               self.cmb_e_typ.get().lower(),
                                                                                               self.ent_e_dom.get()),
                                bg="#cce5ff")

    def bridge_edit_emp(self):
        idx = self.get_tree_idx(self.tree_mgr_emp)
        if idx is None: return
        emp = model.employees[idx]
        for ent in (self.ent_e_imie, self.ent_e_nazwisko, self.ent_e_tel, self.ent_e_dom): ent.delete(0, END)
        self.ent_e_imie.insert(0, emp.imie)
        self.ent_e_nazwisko.insert(0, emp.nazwisko)
        self.ent_e_tel.insert(0, emp.telefon)
        self.ent_e_dom.insert(0, emp.dom)
        self.cmb_e_stanowisko.set(emp.stanowisko)
        self.cmb_e_typ.set("Galeria" if emp.typ_miejsca == "galeria" else "Wystawa")
        self.controller.refresh_all_views()
        self.cmb_e_miejsce.set(emp.miejsce)
        self.btn_e_akcja.config(text="Zapisz zmiany",
                                command=lambda: self.controller.update_employee(idx, self.ent_e_imie.get(),
                                                                                self.ent_e_nazwisko.get(),
                                                                                self.ent_e_tel.get(),
                                                                                self.cmb_e_stanowisko.get(),
                                                                                self.cmb_e_miejsce.get(),
                                                                                self.cmb_e_typ.get().lower(),
                                                                                self.ent_e_dom.get()), bg="#ffe8a1")

    def clear_guest_inputs(self):
        for ent in (self.ent_gst_imie, self.ent_gst_nazwisko, self.ent_gst_tel): ent.delete(0, END)
        self.btn_gst_akcja.config(text="Zapisz wejście",
                                  command=lambda: self.controller.add_guest(self.ent_gst_imie.get(),
                                                                            self.ent_gst_nazwisko.get(),
                                                                            self.ent_gst_tel.get(),
                                                                            self.cmb_gst_bilet.get(),
                                                                            self.cmb_gst_miejsce.get(),
                                                                            self.cmb_gst_typ.get().lower()),
                                  bg="#fff3cd")

    def bridge_edit_gst(self):
        idx = self.get_tree_idx(self.tree_mgr_gst)
        if idx is None: return
        gst = model.guests[idx]
        for ent in (self.ent_gst_imie, self.ent_gst_nazwisko, self.ent_gst_tel): ent.delete(0, END)
        self.ent_gst_imie.insert(0, gst.imie)
        self.ent_gst_nazwisko.insert(0, gst.nazwisko)
        self.ent_gst_tel.insert(0, gst.telefon)
        self.cmb_gst_bilet.set(gst.typ_bilet)
        self.cmb_gst_typ.set("Galeria" if gst.typ_miejsca == "galeria" else "Wystawa")
        self.controller.refresh_all_views()
        self.cmb_gst_miejsce.set(gst.miejsce)
        self.btn_gst_akcja.config(text="Zapisz zmiany",
                                  command=lambda: self.controller.update_guest(idx, self.ent_gst_imie.get(),
                                                                               self.ent_gst_nazwisko.get(),
                                                                               self.ent_gst_tel.get(),
                                                                               self.cmb_gst_bilet.get(),
                                                                               self.cmb_gst_miejsce.get(),
                                                                               self.cmb_gst_typ.get().lower()),
                                  bg="#ffe8a1")


if __name__ == "__main__":
    root = Tk()
    app = ApplicationWindow(root)
    root.mainloop()