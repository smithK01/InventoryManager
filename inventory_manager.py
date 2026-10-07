"""An inventory manager created for CPS 310.
Author: Kalob Smith
Course: CPS 310
"""

INVENTORY = "inventory.txt"

def display_menu():
    """Display a menu for the user to navigate the program"""

    print("\nInventory Manager")
    print("\n")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")
    print("\n")
    return

#def load_inventory(filename):


#def save_inventory(inventory, filename):


#def view_inventory(inventory):


#def add_item(inventory):


#def update_quantity(inventory):


#def remove_item(inventory):


#def search_inventory(inventory):


#def display_summary(inventory):


def main():

    # inventory = load_inventory(INVENTORY)

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            #TODO: view inventory
            None

        elif choice == "2":
            #TODO: add an item
            None

        elif choice == "3":
            #TODO: update an item quantity
            None

        elif choice == "4":
            #TODO: remove an item
            None

        elif choice == "5":
            #TODO: search inventory
            None

        elif choice == "6":
            #TODO: view inventory summary
            None

        elif choice == "7":
            print("\nGoodbye!\n")
            break

        else:
            print("Please enter 1, 2, 3, 4, 5, 6, or 7.")

    return


if __name__ == "__main__":
    main()