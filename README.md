# Inventory Manager

## Description
Inventory Manager is a commandline Python program that tracks items by name, category, and quantity. Inventory data is saved in a local text file for persistence.

## Current Features

- View a numbered inventory with columns for names, categories, and quantities.
- Reject empty name, no category, and negative/non whole number quantities.
- Reject duplicate names, disregarding capitalization.
- Update an item's quantity or remove an item by selecting its displayed number.
- Search for full or partial names disregarding capitalization and leading/trailing whitespace.
- Display a summary of unique names, total quantity of items, low stock items, and item counts by category.
- Load inventory at startup, and save automatically after adding, updating, or removing items.
- Create an empty inventory.txt file if one does not exist.

## Requirements

- Python version 3.12 or newer.
- A terminal, such as Powershell.

## Project Files

| File | Description |
|---|---|
| `inventory_manager.py` | Contains the menu, inventory functions, validation, and file operations. |
| `inventory.txt` | Stores inventory records between program sessions. |
| `README.md` | Explains setup, features, data format, and usage. |
| `TESTING.md` | Documents 14 test cases, expected results, actual results, and pass/fail outcomes. |
| `AI_USAGE.md` | Discloses AI assistance, accepted or modified suggestions, verification, and code understanding. |
| `.gitignore` | Specifies files and folders Git should ignore, such as Python caches and virtual environments. |

## Inventory Data Format

Every line in inventory.txt contains one item, in this order:
name|category|quantity

Names and categories cannot be empty, or contain the pipe ( | ) character. Quantities cannot be negative or non-integers. Blank lines are skipped upon loading.

While running the program stores inventory as a list of dictionaries. Each dictionary has name, category, and quantity keys, with quantity being stored as an integer.

#### Ex:
Laptop Charger|Electronics|8
Printer Paper|Office Supplies|25
Pen|Office Supplies|100
Paper Clip Box|Office Supplies|20
Mouse|Electronics|15
128 GB USB|Electronics|14
USB-C Charger|Electronics|4
Tissue box|Personal Amenities|10

## Running The Program
Using Powershell on Windows 10:
1. download, or clone this repository:
- git clone https://github.com/smithK01/InventoryManager.git
- cd InventoryManager
2. Confirm Python version is 3.12 or newer:
- py --version
3. Start the program:
- py inventory_manager.py

    if that doesn't work, try:

- python inventory_manager.py

## Menu Options
| Option | Action |
|---|---|
| 1. View inventory | Display all items with their item numbers, names, categories, and quantities. |
| 2. Add an item | Enter a new item's name, category, and quantity. |
| 3. Update an item quantity | Select an item number and enter its new quantity. |
| 4. Remove an item | Select an item number to remove that entire record. |
| 5. Search inventory | Enter a full or partial name to display every matching item. |
| 6. View inventory summary | Display unique items, total quantity, low-stock items, and category counts. |
| 7. Exit | Display a goodbye message and end the program. |

## Sample Interaction

python inventory_manager.py

Inventory Manager

1. View inventory
2. Add an item
3. Update an item quantity
4. Remove an item
5. Search inventory
6. View inventory summary
7. Exit

Choose an option: 5

Search: ChArGeR

ChArGeR(s) found:
1. Laptop Charger       | Electronics          | Quantity:     8
2. USB-C Charger        | Electronics          | Quantity:     4

## Testing Summary
TESTING.md documents 14 different cases covering:
- Missing and empty inventory files.
- Adding valid items and rejecting blank or duplicate names.
- Rejecting nonnumeric and negative quantities and accepting zero.
- Updating quantities and rejecting invalid item numbers.
- Removing an item.
- Case-insensitive partial searches and searches with no matches.
- Summary calculations, category grouping, and the low-stock threshold.
- Saving changes and reloading them after restarting.

All 14 tests passed on Windows 10 with Python 3.13.3, as well as passing automated testing on Linux with Python 3.12.14. See [AI_USAGE.md](AI_USAGE.md).

## Git/GitHub Development Summary

Development used incremental commits as features like the menu, file handling, inventory operations, search, summary, and documentation were completed.

The search feature used the feature/inventory-search branch, GitHub issue #1 describing its requirements, and pull request #2 targeting main.

## Known Limitations

- Inventory items must follow the three field format. If bad nonblank lines are manually added to the inventory.txt file, they can stop the program on load.
- The inventory filename is relative to the current working folder.
- display columns use fixed minimum widths. so long names or categories will shift the column alignment, reducing readability.
- Search preserves spaces within the queries, so internal spacing can affect matching.
- The program does not support changing an existing item's name or category unless it is first removed.

## Future Improvements

- Adjust display column widths dynamically to fit stored data better.
- Add ability to cancel from item entry and selection prompts.
- Add a loop to the search_inventory function, so the user can repeat a search without needing to go back to the menu.
- Allow editing names and categories.
- Add sorting and category filters to view_inventory