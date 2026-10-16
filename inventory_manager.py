"""An inventory manager created for CPS 310.
Author: Kalob Smith
Course: CPS 310
"""

INVENTORY_FILE = "inventory.txt"


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


def load_inventory(filename):
    """Check if filename exists, load it's contents.
    Create inventory.txt if filename does not exist.
    Return inventory"""

    inventory = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                else:
                    line_split = line.split("|")
                    inventory_line = {
                        "name": line_split[0].strip(),
                        "category": line_split[1].strip(),
                        "quantity": int(line_split[2].strip()),
                    }
                    inventory.append(inventory_line)

    except FileNotFoundError:
        save_inventory(inventory, filename)

    return inventory


def save_inventory(inventory, filename):
    """Create a new inventory.txt file if none,
    then write contents of list inventory to inventory.txt
    """

    # open/create inventory.txt
    with open(filename, "w", encoding="utf-8") as file:

        # for every dictionary in inventory[]
        for line in inventory:
            line_to_string = f"{line['name']}|{line['category']}|{line['quantity']}\n"
            file.write(line_to_string)


def view_inventory(inventory):
    """For every dictionary in inventory, print to terminal"""

    if not inventory:
        print("No inventory items found.")
    else:
        for i, line in enumerate(inventory):
            # :< , :> left align and right align
            print(
                f"{i+1}. {line["name"]:<20} | {line["category"]:<20} | Quantity: {line["quantity"]:>5}"
            )


def add_item(inventory):
    """Ask user for name, category, and quantity of an item.
    create dictionary of item, and append to inventory.txt"""

    is_good_input = False

    while True:
        print("Enter the name of the item: ")
        new_item_name = input().strip()
        if new_item_name == "" or "|" in new_item_name:
            print("Invalid name")
            continue
        for i in inventory:
            if i["name"].lower() == new_item_name.lower():
                print(f"{new_item_name} already found in inventory")
                break

        else:
            print(f"Enter the category {new_item_name} belongs to: ")
            new_item_category = input().strip()

            if new_item_category == "" or "|" in new_item_category:
                print("Invalid category")
                continue
            else:
                quantity_loop = True
                while quantity_loop == True:
                    print(f"Enter the quantity of {new_item_name}(s): ")
                    new_item_amount = input().strip()
                    try:
                        int_new_item_amount = int(new_item_amount)
                        if int_new_item_amount < 0:
                            raise ValueError
                        is_good_input = True
                        quantity_loop = False
                    except ValueError:
                        print(
                            "Please enter a whole number greater than or equal to zero."
                        )
                        continue
        if is_good_input == True:
            new_inventory_item = {
                "name": new_item_name,
                "category": new_item_category,
                "quantity": int_new_item_amount,
            }
            inventory.append(new_inventory_item)
            print(f"{new_inventory_item} added to inventory.")
            save_inventory(inventory, INVENTORY_FILE)
            return


def update_quantity(inventory):
    """Update a quantity of an item in inventory, then save updated
    quantity to inventory"""

    if not inventory:
        print("inventory empty.")
        return

    while True:
        view_inventory(inventory)
        selection = input("Enter the item number to update: ")
        try:
            selection = int(selection)
            if selection > len(inventory) or selection <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid integer.")
            continue

        quantity_change = input("Enter the new quantity: ")
        try:
            quantity_change = int(quantity_change)
            if quantity_change < 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid, non negative integer.")
            continue
        selected_item = inventory[selection - 1]
        selected_item["quantity"] = quantity_change
        save_inventory(inventory, INVENTORY_FILE)
        print(f"{selected_item["name"]}(s) quantity updated to {quantity_change}")
        return


def remove_item(inventory):
    """Remove an item from inventory, confirm removed item, save to inventory"""

    view_inventory(inventory)
    if not inventory:
        return

    while True:
        selected_item = input("Enter the item number to remove: ")
        try:
            selected_item = int(selected_item)
            if selected_item > len(inventory) or selected_item <= 0:
                raise ValueError

        except ValueError:
            print("Enter a valid inventory number.")
            continue

        item_to_remove = inventory.pop(selected_item - 1)
        save_inventory(inventory, INVENTORY_FILE)
        print(f"Item removed: {item_to_remove["name"]}")
        return


def search_inventory(inventory):
    """Search inventory dictionaries for exact and partial matching names.
    Display error message if no items match the search."""

    if not inventory:
        print("Inventory empty.")
        return

    item_found = False
    item_matches = []

    search_query = input("\nSearch: ").strip()
    if search_query != "":
        for i in inventory:
            if search_query.lower() in i["name"].lower():
                item_found = True
                item_matches.append(i)
    else:
        print("Please enter a valid search.")
        return

    if item_found:
        print(f"\n{search_query}(s) found:")
        view_inventory(item_matches)
    else:
        print(f"No {search_query}(s) found.")

    return


def display_summary(inventory):
    """display a summary of inventory, listing unique items, total quantity
    items below 5 quantity, and items by category"""

    total_items = 0
    unique_items = 0
    low_stock_items = 0
    categories = {}
    unique_item_names = []

    if not inventory:
        print("Inventory empty")

    for i in inventory:

        total_items = total_items + int(i["quantity"])

        if i["name"].lower() not in unique_item_names:
            unique_item_names.append(i["name"].lower())
            unique_items = unique_items + 1

        category = i["category"].lower()
        if category not in categories:
            categories[category] = 1
        else:
            categories[category] += 1

        if int(i["quantity"]) < 5:
            low_stock_items = low_stock_items + 1

    print("Inventory Summary")
    print(f"Unique items: {unique_items}")
    print(f"Total quantity: {total_items}")
    print(f"Low-stock items: {low_stock_items}")
    print("\n")
    print("Items by category:")
    for category in categories:
        print(f"{category}: {categories[category]}")


def main():
    """Main entry to program"""

    # if inventory.txt exists, load it, else, create it
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_inventory(inventory)

        elif choice == "2":
            add_item(inventory)

        elif choice == "3":
            update_quantity(inventory)

        elif choice == "4":
            remove_item(inventory)

        elif choice == "5":
            search_inventory(inventory)

        elif choice == "6":
            display_summary(inventory)

        elif choice == "7":
            print("\nGoodbye!\n")
            break

        else:
            print("Please enter 1, 2, 3, 4, 5, 6, or 7.")

    return


if __name__ == "__main__":
    main()
