import gallery_lib.model as model
import gallery_lib.controller as controller


def main():
    while True:
        print("==========MENU==========")
        print("0 - zakończ program")
        print("1 - wyświetl dane (Galerie, Wystawy, Kadry, Goście)")
        print("2 - dodanie elementu")
        print("3 - usuwanie elementu")
        print("4 - update elementu")
        print("5 - pokaż mapę lokalizacji")

        choice = input("Wybierz opcje w menu: ")
        print(f"Wybrano opcję {choice}")

        if choice == "0":
            break

        if choice == "1":
            print("\n--- GALERIE ---")
            controller.read_galleries(model.galleries_list)
            print("\n--- WYSTAWY ---")
            controller.read_exhibitions(model.exhibitions_list)
            print("\n--- PRACOWNICY ---")
            controller.read_employees(model.employees_list)
            print("\n--- GOŚCIE ---")
            controller.read_guests(model.guests_list)

        if choice == "2":
            kat = input("Co chcesz dodać? (1 - galeria, 2 - wystawa, 3 - pracownik, 4 - gość): ")
            if kat == "1": controller.add_gallery(model.galleries_list)
            if kat == "2": controller.add_exhibition(model.exhibitions_list)
            if kat == "3": controller.add_employee(model.employees_list)
            if kat == "4": controller.add_guest(model.guests_list)

        if choice == "3":
            kat = input("Co chcesz usunąć? (1 - galeria, 2 - wystawa, 3 - pracownik, 4 - gość): ")
            if kat == "1": controller.remove_gallery(model.galleries_list)
            if kat == "2": controller.remove_exhibition(model.exhibitions_list)
            if kat == "3": controller.remove_employee(model.employees_list)
            if kat == "4": controller.remove_guest(model.guests_list)

        if choice == "4":
            kat = input("Co chcesz zaktualizować? (1 - galeria, 2 - wystawa, 3 - pracownik, 4 - gość): ")
            if kat == "1": controller.update_gallery(model.galleries_list)
            if kat == "2": controller.update_exhibition(model.exhibitions_list)
            if kat == "3": controller.update_employee(model.employees_list)
            if kat == "4": controller.update_guest(model.guests_list)

        if choice == "5":
            controller.get_map(model.galleries_list, model.exhibitions_list)


if __name__ == "__main__":
    main()