"""test suite for inventory_manager"""

from copy import deepcopy

import pytest

from inventory_manager import (
    calculate_summary,
    find_matching_items,
    load_inventory,
    remove_item_by_number,
    save_inventory,
    update_item_quantity,
    validate_new_item,
)

VALID_INVENTORY_TEXT = (
    "Laptop Charger|Electronics|4\n"
    "USB-C Charger|electronics|5\n"
    "Pen|Office Supplies|10\n"
    "Notebook|Office Supplies|0\n"
)


@pytest.fixture
def sample_inventory():
    """sample inventory for repeatability in test cases"""

    return [
        {"name": "Laptop Charger", "category": "Electronics", "quantity": 4},
        {"name": "USB-C Charger", "category": "electronics", "quantity": 5},
        {"name": "Pen", "category": "Office Supplies", "quantity": 10},
        {"name": "Notebook", "category": "Office Supplies", "quantity": 0},
    ]


def test_load_inventory_from_valid_file(tmp_path, sample_inventory):
    """load an expected list of dicts from inv file"""

    # Arrange
    inventory_file = tmp_path / "inventory.txt"
    inventory_file.write_text(VALID_INVENTORY_TEXT, encoding="utf-8")

    # Act
    actual = load_inventory(inventory_file)

    # Assert
    assert actual == sample_inventory


def test_load_inventory_converts_quantities_to_integers(tmp_path):
    """chaange all inventory quantities to int with no value errors"""

    # Arrange
    inventory_file = tmp_path / "inventory.txt"
    inventory_file.write_text(VALID_INVENTORY_TEXT, encoding="utf-8")

    # Act
    actual = load_inventory(inventory_file)

    # Assert
    assert [item["quantity"] for item in actual] == [4, 5, 10, 0]
    assert all(type(item["quantity"]) is int for item in actual)


def test_load_inventory_ignores_blank_lines(tmp_path, sample_inventory):
    """ignore empty and whitespace in inventory file"""

    # Arrange
    inventory_file = tmp_path / "inventory.txt"
    text_with_blanks = "\n \t\n" + VALID_INVENTORY_TEXT.replace("\n", "\n\n")
    inventory_file.write_text(text_with_blanks, encoding="utf-8")

    # Act
    actual = load_inventory(inventory_file)

    # Assert
    assert actual == sample_inventory


def test_load_inventory_missing_file_returns_empty_list(tmp_path):
    """dont crash on missing inv file"""

    # Arrange
    missing_file = tmp_path / "missing_inventory.txt"

    # Act
    actual = load_inventory(missing_file)

    # Assert
    assert actual == []


def test_save_inventory_writes_multiple_items_in_correct_format(
    tmp_path, sample_inventory
):
    """write one pipe seperated item per line."""

    # Arrange
    inventory_file = tmp_path / "inventory.txt"

    # Act
    save_inventory(sample_inventory, inventory_file)

    # Assert
    assert inventory_file.read_text(encoding="utf-8") == VALID_INVENTORY_TEXT


def test_save_inventory_empty_list_creates_empty_file(tmp_path):
    """saving empty list should clear a full old list"""

    # Arrange
    inventory_file = tmp_path / "inventory.txt"
    inventory_file.write_text("Old Item|Old Category|99\n", encoding="utf-8")

    # Act
    save_inventory([], inventory_file)

    # Assert
    assert inventory_file.read_text(encoding="utf-8") == ""


def test_save_and_load_inventory_round_trip(tmp_path, sample_inventory):
    """make sure data is actually saved and loaded in a round trip"""

    # Arrange
    inventory_file = tmp_path / "inventory.txt"
    expected = deepcopy(sample_inventory)

    # Act
    save_inventory(sample_inventory, inventory_file)
    actual = load_inventory(inventory_file)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    "search_term",
    [
        "Laptop Charger",
        "laptop charger",
        "LAPTOP CHARGER",
        "lApToP cHaRgEr",
        "  Laptop Charger  ",
    ],
    ids=["exact", "lowercase", "uppercase", "mixed-case", "surrounding-spaces"],
)
def test_search_exact_name_ignores_case(sample_inventory, search_term):
    """Find an exact name, dont care about caps or case/whitespace"""

    # Arrange
    original = deepcopy(sample_inventory)
    expected = [original[0]]

    # Act
    actual = find_matching_items(sample_inventory, search_term)

    # Assert
    assert actual == expected
    assert sample_inventory == original


def test_search_returns_multiple_partial_matches(sample_inventory):
    """return all items even partials that match actual items."""

    # Arrange
    original = deepcopy(sample_inventory)
    search_term = "charger"
    expected = original[:2]

    # Act
    actual = find_matching_items(sample_inventory, search_term)

    # Assert
    assert actual == expected
    assert sample_inventory == original


def test_search_with_no_matches_returns_empty_list(sample_inventory):
    """Return an empty list when no item matches a search."""

    # Arrange
    original = deepcopy(sample_inventory)
    search_term = "wrench"

    # Act
    actual = find_matching_items(sample_inventory, search_term)

    # Assert
    assert actual == []
    assert sample_inventory == original


@pytest.mark.parametrize(
    "search_term",
    ["", "   ", " \t\n "],
    ids=["empty", "spaces-only", "mixed-whitespace"],
)
def test_search_rejects_empty_and_whitespace_queries(sample_inventory, search_term):
    """return bad input result for empty searches."""

    # Arrange
    original = deepcopy(sample_inventory)

    # Act
    actual = find_matching_items(sample_inventory, search_term)

    # Assert
    assert actual is None
    assert sample_inventory == original


@pytest.mark.parametrize(
    "item_number, expected_name, expected_remaining_names",
    [
        (1, "Laptop Charger", ["USB-C Charger", "Pen", "Notebook"]),
        (2, "USB-C Charger", ["Laptop Charger", "Pen", "Notebook"]),
        (4, "Notebook", ["Laptop Charger", "USB-C Charger", "Pen"]),
    ],
    ids=["first-item", "middle-item", "last-item"],
)
def test_remove_first_middle_and_last_item(
    sample_inventory, item_number, expected_name, expected_remaining_names
):
    """Return item, other stuff should still be in order and the same"""

    # Arrange
    original_by_name = {item["name"]: item for item in deepcopy(sample_inventory)}
    expected_removed = original_by_name[expected_name]
    expected_remaining = [original_by_name[name] for name in expected_remaining_names]

    # Act
    actual = remove_item_by_number(sample_inventory, item_number)

    # Assert
    assert actual == expected_removed
    assert sample_inventory == expected_remaining


@pytest.mark.parametrize(
    "item_number",
    [0, -1, 5],
    ids=["zero", "negative", "above-inventory-length"],
)
def test_remove_rejects_invalid_item_numbers(sample_inventory, item_number):
    """Reject bad selections, dont change anything else."""

    # Arrange
    original = deepcopy(sample_inventory)

    # Act
    actual = remove_item_by_number(sample_inventory, item_number)

    # Assert
    assert actual is None
    assert sample_inventory == original


@pytest.mark.parametrize(
    "new_quantity",
    [0, 12],
    ids=["zero-quantity", "positive-quantity"],
)
def test_update_quantity_changes_only_selected_item(sample_inventory, new_quantity):
    """take zero and positive quantities dont change anything else."""

    # Arrange
    expected = deepcopy(sample_inventory)
    expected[1]["quantity"] = new_quantity

    # Act
    actual = update_item_quantity(sample_inventory, 2, new_quantity)

    # Assert
    assert actual == expected[1]
    assert sample_inventory == expected


@pytest.mark.parametrize(
    "item_number",
    [0, -1, 5],
    ids=["zero", "negative", "above-inventory-length"],
)
def test_update_quantity_rejects_invalid_item_numbers(sample_inventory, item_number):
    """Reject invalid item numbers without modifying anything"""

    # Arrange
    original = deepcopy(sample_inventory)

    # Act
    actual = update_item_quantity(sample_inventory, item_number, 8)

    # Assert
    assert actual == "bad_item_number"
    assert sample_inventory == original


def test_update_quantity_rejects_negative_quantity(sample_inventory):
    """dump a negative quantity and don't change original inventory."""

    # Arrange
    original = deepcopy(sample_inventory)

    # Act
    actual = update_item_quantity(sample_inventory, 2, -1)

    # Assert
    assert actual == "bad_quantity"
    assert sample_inventory == original


@pytest.mark.parametrize(
    "name, category, quantity, expected",
    [
        (
            "HDMI Cable",
            "Electronics",
            "6",
            {"name": "HDMI Cable", "category": "Electronics", "quantity": 6},
        ),
        (
            "Cable",
            "Electronics",
            0,
            {"name": "Cable", "category": "Electronics", "quantity": 0},
        ),
        (
            "  HDMI Cable  ",
            " Electronics ",
            6,
            {"name": "HDMI Cable", "category": "Electronics", "quantity": 6},
        ),
        ("", "Electronics", 2, "invalid_name"),
        ("   ", "Electronics", 2, "invalid_name"),
        ("Cable", "", 2, "invalid_category"),
        ("Cable", "   ", 2, "invalid_category"),
        ("Cable|Adapter", "Electronics", 2, "invalid_name"),
        ("Cable", "Electronics|Office", 2, "invalid_category"),
        ("Cable", "Electronics", -1, "invalid_quantity"),
        ("Cable", "Electronics", "many", "invalid_quantity"),
        ("Cable", "Electronics", "1.5", "invalid_quantity"),
        ("Laptop Charger", "Electronics", 2, "duplicate_of_existing_item"),
        ("lApToP cHaRgEr", "Electronics", 2, "duplicate_of_existing_item"),
        (" Laptop Charger ", "Electronics", 2, "duplicate_of_existing_item"),
    ],
    ids=[
        "valid-item",
        "valid-zero-quantity",
        "trimmed-name-and-category",
        "empty-name",
        "whitespace-name",
        "empty-category",
        "whitespace-category",
        "pipe-in-name",
        "pipe-in-category",
        "negative-quantity",
        "nonnumeric-quantity",
        "fractional-quantity-text",
        "duplicate-name",
        "duplicate-mixed-case",
        "duplicate-surrounding-spaces",
    ],
)
def test_validate_new_item_rules(sample_inventory, name, category, quantity, expected):
    """confirm new item inputs without appending to inventory."""

    # Arrange
    original = deepcopy(sample_inventory)

    # Act
    actual = validate_new_item(sample_inventory, name, category, quantity)

    # Assert
    assert actual == expected
    assert sample_inventory == original


def test_calculate_summary_values(sample_inventory):
    """Calc totals and put similar category names together without caring about case."""

    # Arrange
    original = deepcopy(sample_inventory)
    expected = (
        4,
        19,
        2,
        {"electronics": 2, "office supplies": 2},
        ["laptop charger", "usb-c charger", "pen", "notebook"],
    )

    # Act
    actual = calculate_summary(sample_inventory)

    # Assert
    assert actual == expected
    assert sample_inventory == original


def test_calculate_summary_empty_inventory():
    """zero totals and empty collections for an empty inventory"""

    # Arrange
    inventory = []
    expected = (0, 0, 0, {}, [])

    # Act
    actual = calculate_summary(inventory)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    "quantity, expected_low_stock",
    [(4, 1), (5, 0)],
    ids=["four-is-low-stock", "five-is-not-low-stock"],
)
def test_calculate_summary_low_stock_boundary(quantity, expected_low_stock):
    """less than 5 threshold"""

    # Arrange
    inventory = [{"name": "Boundary Item", "category": "Test", "quantity": quantity}]

    # Act
    actual = calculate_summary(inventory)

    # Assert
    assert actual[2] == expected_low_stock
