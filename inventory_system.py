"""Inventory system module.

Provides functions and classes to manage inventory items, stock levels,
and related operations.
"""
import json
from datetime import datetime
from typing import Dict, List, Optional

stock_data: Dict[str, int] = {}


def add_item(
    item: str = "default",
    qty: int = 0,
    logs: Optional[List[str]] = None,
) -> None:
    """Add qty of item to stock_data and optionally append a log entry.

    Args:
        item: Item name (string).
        qty: Quantity to add (will be coerced to int).
        logs: Optional list to append a log entry to.
    """
    if logs is None:
        logs = []
    if not item:
        return
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    try:
        qty = int(qty)
    except (TypeError, ValueError) as exc:
        raise TypeError("qty must be an integer") from exc
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item: str, qty: int) -> None:
    """Remove qty of item from stock_data; delete item if quantity <= 0.

    If the item is not present, the function returns silently.
    """
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    try:
        qty = int(qty)
    except (TypeError, ValueError) as exc:
        raise TypeError("qty must be an integer") from exc
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        pass


def get_qty(item: str) -> int:
    """Return quantity for item; returns 0 if item not present."""
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load stock_data from a JSON file. If file missing, do nothing."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    if not isinstance(data, dict):
        raise ValueError("inventory file must contain a JSON object")
    stock_data.clear()
    for k, v in data.items():
        try:
            stock_data[str(k)] = int(v)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid quantity for item {k}") from exc


def save_data(file: str = "inventory.json") -> None:
    """Save stock_data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, ensure_ascii=False, indent=2)


def print_data() -> None:
    """Print a simple items report to stdout."""
    print("Items Report")
    for item, qty in stock_data.items():
        print(item, "->", qty)


def check_low_items(threshold: int = 5) -> List[str]:
    """Return a list of items with quantity below the threshold."""
    try:
        threshold = int(threshold)
    except (TypeError, ValueError) as exc:
        raise TypeError("threshold must be an integer") from exc
    return [item for item, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Example script run demonstrating the inventory functions."""
    logs: List[str] = []
    add_item("apple", 10, logs)
    add_item("banana", 2, logs)
    try:
        add_item(123, "ten", logs)
    except TypeError:
        logs.append(f"{datetime.now()}: Ignored invalid add_item call")
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    logs.append(f"{datetime.now()}: main completed")
    for entry in logs:
        print(entry)


main()
