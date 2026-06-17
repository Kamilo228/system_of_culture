import gallery_lib.model as model


class AppController:
    def __init__(self, view):
        self.view = view

        # Flagi sprawdzające, czy jesteśmy w trybie widoku szczegółów danej galerii/wystawy
        self.in_g_details = False
        self.in_ex_details = False

        # Mapowanie indeksów wyszukiwania na prawdziwe indeksy obiektów w bazie
        self.g_map_idx = []
        self.ex_map_idx = []

    def refresh_all_views(self):
        """Koordynuje i odświeża wszystkie listy, drzewa oraz dropdowny w systemie."""
        g_szukaj = self.view.get_search_gallery_text().lower()
        ex_szukaj = self.view.get_search_exhibition_text().lower()

        # 1. Filtrowanie i aktualizacja Listboxa Galerii
        self.g_map_idx = [i for i, g in enumerate(model.galleries) if
                          g_szukaj in g.nazwa.lower() or g_szukaj in g.lokalizacja.lower()]
        g_items = [f"{model.galleries[i].nazwa} ({model.galleries[i].lokalizacja})" for i in self.g_map_idx]
        if not self.in_g_details:
            self.view.update_gallery_listbox(g_items, [model.galleries[i] for i in self.g_map_idx])

        # 2. Filtrowanie i aktualizacja Listboxa Wystaw
        self.ex_map_idx = [i for i, ex in enumerate(model.exhibitions) if
                           ex_szukaj in ex.nazwa.lower() or ex_szukaj in ex.lokalizacja.lower()]
        ex_items = [f"{model.exhibitions[i].nazwa} ({model.exhibitions[i].lokalizacja})" for i in self.ex_map_idx]
        if not self.in_ex_details:
            self.view.update_exhibition_listbox(ex_items, [model.exhibitions[i] for i in self.ex_map_idx])

        # 3. Aktualizacja bazy kadr i gości w panelu zarządzania
        self.view.update_management_trees(model.employees, model.guests)

        # 4. Odświeżenie list rozwijanych (Combobox) w formularzach
        g_names = [g.nazwa for g in model.galleries]
        ex_names = [ex.nazwa for ex in model.exhibitions]
        self.view.refresh_dropdown_options(g_names, ex_names)

    # --- OBSŁUGA GALERII ---
    def add_gallery(self, nazwa, typ, lok):
        if nazwa and typ and lok:
            model.galleries.append(model.Gallery(nazwa, typ, lok))
            self.refresh_all_views()
            self.view.clear_gallery_inputs()

    def remove_gallery(self, list_idx, has_selection):
        if not has_selection or self.in_g_details: return
        real_idx = self.g_map_idx[list_idx]
        model.galleries.pop(real_idx)
        self.refresh_all_views()

    def edit_gallery_clicked(self, list_idx, has_selection):
        if not has_selection or self.in_g_details: return
        real_idx = self.g_map_idx[list_idx]
        self.view.populate_gallery_inputs(model.galleries[real_idx], real_idx)

    def save_gallery_update(self, real_idx, nazwa, typ, lok):
        if nazwa and typ and lok:
            g = model.galleries[real_idx]
            g.nazwa, g.typ_sztuki, g.lokalizacja = nazwa, typ, lok
            g.coordinates = g.get_coordinates()
            self.refresh_all_views()
            self.view.clear_gallery_inputs()

    def gallery_selected(self, list_idx):
        if self.in_g_details or not self.g_map_idx: return
        real_idx = self.g_map_idx[list_idx]
        self.view.move_map_to("galeria", model.galleries[real_idx].coordinates)

    def toggle_gallery_details(self, list_idx, has_selection):
        if self.in_g_details:
            self.in_g_details = False
            self.view.clear_gallery_details_view()
            self.refresh_all_views()
        elif has_selection:
            self.in_g_details = True
            g = model.galleries[self.g_map_idx[list_idx]]
            g_emps = [e for e in model.employees if e.miejsce == g.nazwa and e.typ_miejsca == "galeria"]
            g_gsts = [g_obj for g_obj in model.guests if g_obj.miejsce == g.nazwa and g_obj.typ_miejsca == "galeria"]
            self.view.show_gallery_details_view(g, g_emps, g_gsts)

    def search_gallery_changed(self):
        self.view.reset_gallery_details_button()
        self.in_g_details = False
        self.refresh_all_views()

    # --- OBSŁUGA WYSTAW ---
    def add_exhibition(self, nazwa, temat, lok):
        if nazwa and temat and lok:
            model.exhibitions.append(model.Exhibition(nazwa, temat, lok))
            self.refresh_all_views()
            self.view.clear_exhibition_inputs()

    def remove_exhibition(self, list_idx, has_selection):
        if not has_selection or self.in_ex_details: return
        real_idx = self.ex_map_idx[list_idx]
        model.exhibitions.pop(real_idx)
        self.refresh_all_views()

    def edit_exhibition_clicked(self, list_idx, has_selection):
        if not has_selection or self.in_ex_details: return
        real_idx = self.ex_map_idx[list_idx]
        self.view.populate_exhibition_inputs(model.exhibitions[real_idx], real_idx)

    def save_exhibition_update(self, real_idx, nazwa, temat, lok):
        if nazwa and temat and lok:
            ex = model.exhibitions[real_idx]
            ex.nazwa, ex.tematyka, ex.lokalizacja = nazwa, temat, lok
            ex.coordinates = ex.get_coordinates()
            self.refresh_all_views()
            self.view.clear_exhibition_inputs()

    def exhibition_selected(self, list_idx):
        if self.in_ex_details or not self.ex_map_idx: return
        real_idx = self.ex_map_idx[list_idx]
        self.view.move_map_to("wystawa", model.exhibitions[real_idx].coordinates)

    def toggle_exhibition_details(self, list_idx, has_selection):
        if self.in_ex_details:
            self.in_ex_details = False
            self.view.clear_exhibition_details_view()
            self.refresh_all_views()
        elif has_selection:
            self.in_ex_details = True
            ex = model.exhibitions[self.ex_map_idx[list_idx]]
            ex_emps = [e for e in model.employees if e.miejsce == ex.nazwa and e.typ_miejsca == "wystawa"]
            ex_gsts = [g for g in model.guests if g.miejsce == ex.nazwa and g.typ_miejsca == "wystawa"]
            self.view.show_exhibition_details_view(ex, ex_emps, ex_gsts)

    def search_exhibition_changed(self):
        self.view.reset_exhibition_details_button()
        self.in_ex_details = False
        self.refresh_all_views()

    # --- PANEL ZARZĄDZANIA (KADRY I GOŚCIE) ---
    def add_employee(self, imie, nazwisko, tel, stan, miejsce, typ, dom):
        if imie and nazwisko and tel and miejsce and dom:
            model.employees.append(model.Employee(imie, nazwisko, tel, stan, miejsce, typ, dom))
            self.refresh_all_views()
            self.view.clear_employee_inputs()

    def remove_employee(self, idx):
        if idx is not None:
            model.employees.pop(idx)
            self.refresh_all_views()

    def update_employee(self, idx, imie, nazwisko, tel, stan, miejsce, typ, dom):
        if imie and nazwisko and tel and miejsce and dom:
            emp = model.employees[idx]
            emp.imie, emp.nazwisko, emp.telefon, emp.stanowisko = imie, nazwisko, tel, stan
            emp.miejsce, emp.typ_miejsca, emp.dom = miejsce, typ, dom
            emp.coordinates = emp.get_coordinates()
            self.refresh_all_views()
            self.view.clear_employee_inputs()

    def employee_selected(self, idx):
        if idx is None: return
        emp = model.employees[idx]
        self.view.set_management_details_text(
            f"Pracownik: {emp.imie} {emp.nazwisko} | Stanowisko: {emp.stanowisko}\nPrzypisanie: {emp.miejsce} ({emp.typ_miejsca}) | Dom: {emp.dom}")
        self.view.move_map_to("zarzadzanie", emp.coordinates)

    def add_guest(self, imie, nazwisko, tel, bilet, miejsce, typ):
        if imie and nazwisko and tel and miejsce:
            model.guests.append(model.Guest(imie, nazwisko, tel, bilet, miejsce, typ))
            self.refresh_all_views()
            self.view.clear_guest_inputs()

    def remove_guest(self, idx):
        if idx is not None:
            model.guests.pop(idx)
            self.refresh_all_views()

    def update_guest(self, idx, imie, nazwisko, tel, bilet, miejsce, typ):
        if imie and nazwisko and tel and miejsce:
            gst = model.guests[idx]
            gst.imie, gst.nazwisko, gst.telefon, gst.typ_bilet, gst.miejsce, gst.typ_miejsca = imie, nazwisko, tel, bilet, miejsce, typ
            self.refresh_all_views()
            self.view.clear_guest_inputs()

    def guest_selected(self, idx):
        if idx is None: return
        gst = model.guests[idx]
        self.view.set_management_details_text(
            f"Gość: {gst.imie} {gst.nazwisko} | Bilet: {gst.typ_bilet}\nMiejsce wizyty: {gst.miejsce} ({gst.typ_miejsca}) | Telefon: {gst.telefon}")