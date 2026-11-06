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

    while True:
        print("Enter the name of the item: ")
        new_item_name = input()
        print(f"Enter the category {new_item_name} belongs to: ")
        category = input()
        print(f"Enter the quantity of {new_item_name}(s): ")
        quantity = input()

        new_item = validate_new_item(inventory, new_item_name, category, quantity)

        if new_item == "invalid_name":
            print("Please enter a valid item name")
        elif new_item == "invalid_category":
            print("Please enter a valid category name.")
        elif new_item == "invalid_quantity":
            print("Please enter a valid nonnegative quantity.")
        elif new_item == "duplicate_of_existing_item":
            print(f"{new_item_name} already in inventory.")
        else:

            inventory.append(new_item)
            print(f"{new_item_name} added to inventory.")
            
            save_inventory(inventory, INVENTORY_FILE)
            return


# add_item() helper
def validate_new_item(inventory, name, category, quantity):
    """validate input of new item name, category, and quantity
    Return error values if invalid, otherwise return new_inventory_item dictionary"""

    name = name.strip()
    category = category.strip()
    # quantity handled in last else condition

    if name == "" or "|" in name:
        return "invalid_name"
    
    for i in inventory:
        if i["name"].lower() == name.lower():
            return "duplicate_of_existing_item"

    else:
        if category == "" or "|" in category:
            return "invalid_category"
        
        else:
            try:
                int_quantity = int(quantity)
                if int_quantity < 0:
                    raise ValueError
            except ValueError:
                return "invalid_quantity"

    # every check is good
    new_inventory_item = {
        "name": name,
        "category": category,
        "quantity": int_quantity,
    }
        
    return new_inventory_item


def update_quantity(inventory):
    """Update a quantity of an item in inventory, then save updated
    quantity to inventory"""

    if not inventory:
        print("inventory empty.")
        return

    while True:
        view_inventory(inventory)
        selection = input("Enter the item number to update: ")
        quantity_change = input("Enter the new quantity: ")

        selected_item = update_item_quantity(inventory, selection, quantity_change)

        if selected_item == "bad_quantity" or selected_item == "bad_item_number":
            print("Please enter valid, non negative integers.")
        else:
            save_inventory(inventory, INVENTORY_FILE)
            print(f"{selected_item["name"]}(s) quantity updated to {selected_item["quantity"]}")
            return


# update_quantity() helper
def update_item_quantity(inventory, item_number, new_quantity):
    """take item_number, new_quantity, verify they are nonnegative integers
    Return error string if bad input, return selected_item updated otherwise"""

    try:
        item_number = int(item_number)
        if item_number > len(inventory) or item_number <= 0:
            raise ValueError
    except ValueError:
        return "bad_item_number"

    try:
        new_quantity = int(new_quantity)
        if new_quantity < 0:
            raise ValueError
    except ValueError:
        return "bad_quantity"

    selected_item = inventory[item_number - 1]
    selected_item["quantity"] = new_quantity

    return selected_item


def remove_item(inventory):
    """Remove an item from inventory, confirm removed item, save to inventory"""

    while True:
        view_inventory(inventory)
        if not inventory:
            return
        selected_item = input("Enter the item number to remove: ")
        removed_item = remove_item_by_number(inventory, selected_item)

        if removed_item:
            print(f"Item removed: {removed_item["name"]}")
            save_inventory(inventory, INVENTORY_FILE)
            return
        else:
            print("Enter a valid inventory number.")
            continue


# remove_item() helper
def remove_item_by_number(inventory, item_number):
    """Attempt to remove item_number from inventory
    return removed item, or none"""

    try:
        item_number = int(item_number)
        if item_number > len(inventory) or item_number <= 0:
            raise ValueError
        return inventory.pop(item_number - 1)

    except ValueError:
        return None


def search_inventory(inventory):
    """Take input, send to find_matching_items(), print message
    showing found item or none"""

    if not inventory:
        print("Inventory empty.")
        return

    search_query = input("\nSearch: ")
    any_matches = find_matching_items(inventory, search_query)
    try:
        if len(any_matches) > 0:
            print(f"\n{search_query}(s) found:")
            view_inventory(any_matches)
        else:
            print(f"no {search_query}(s) found.")
    except TypeError:
        print(f"Please enter a valid search.")
    return


# search_inventory() helper
def find_matching_items(inventory, search_query):
    """Search inventory dictionaries for exact and partial matching names.
    Return item_matches with found searches, empty, or None for bad input."""

    search_query = search_query.strip()
    item_matches = []

    if search_query != "":
        for i in inventory:
            if search_query.lower() in i["name"].lower():
                item_matches.append(i)
    else:
        return None
    return item_matches


def display_summary(inventory):
    """display a summary of inventory, listing unique items, total quantity
    items below 5 quantity, and items by category"""

    # need a tuple for multiple returning values in one return statement
    summary_tuple = calculate_summary(inventory)

    if summary_tuple == None:
        print("No inventory found.")
    else:
        print("\nInventory Summary")
        print(f"Unique items: {summary_tuple[0]}")
        print(f"Total quantity: {summary_tuple[1]}")
        print(f"Low-stock items: {summary_tuple[2]}")
        print("\n")
        print("Items by category:")
        for category in summary_tuple[3]:
            print(f"{category}: {summary_tuple[3][category]}")


# display_summary() helper
def calculate_summary(inventory):
    """Return a summary of inventory, with unique items, total quantity,
    items below 5 quantity, and items by category in a tuple"""

    unique_items = 0
    total_items = 0
    low_stock_items = 0
    categories = {}
    unique_item_names = []

    if not inventory:
        summary_tuple = (unique_items, total_items, low_stock_items, categories, unique_item_names)
        return summary_tuple
    
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

    summary_tuple = (unique_items, total_items, low_stock_items, categories, unique_item_names)

    return summary_tuple


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
