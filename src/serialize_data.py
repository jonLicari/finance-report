import json
import os
from decimal import Decimal

from expense_class import Cashflow, SerializedCashflow


def decimal_to_string(value: Decimal) -> str:
    """Convert Decimal type to string."""
    return str(value)


def decimal_to_float(value: Decimal) -> float:
    """Convert Decimal type to float."""
    return float(value)


def serialize(dollars: Decimal, string_format: bool) -> str | float:
    """Serialize Decimal-type to a standard format."""
    if string_format:
        return decimal_to_string(dollars)

    return decimal_to_float(dollars)


def serialize_categories(primary: dict[str, Decimal], string_format=True) -> dict:
    """Convert category data to serializable format."""
    primary_serial = {
        key: serialize(value, string_format) for key, value in primary.items()
    }
    return primary_serial


def serialize_subcategories(
    secondary: dict[str, dict[str, Decimal]], string_format=True
) -> dict:
    """Convert subcategory data to serializable format."""
    secondary_serial = {
        key: {sub_key: serialize(value[sub_key], string_format) for sub_key in value}
        for key, value in secondary.items()
    }
    return secondary_serial


def serialize_cashflow(item: Cashflow, string_format=True) -> SerializedCashflow:
    """Convert cashflow data to serializable format."""

    return SerializedCashflow(
        serialize(item.ingoing, string_format), serialize(item.outgoing, string_format)
    )


def create_export_file(json_data, name: str):
    """Create JSON file and write data to it."""
    path = os.getcwd() + "/data/output/"
    extension = ".json"

    with open(path + name + extension, "w") as file:
        file.write(json_data)
    file.close()


def export_all_to_json(
    ytd: Cashflow,
    per_month: list[Cashflow],
    category: dict[str, Decimal],
    subcategory: dict[str, dict[str, Decimal]],
) -> None:
    """Serialize data, pack into JSON format, export."""

    # Serialize All Data
    ytd_s = serialize_cashflow(ytd)
    monthly_s: list[SerializedCashflow] = [
        serialize_cashflow(item) for item in per_month
    ]
    primary_s = serialize_categories(category)
    secondary_s = serialize_subcategories(subcategory)

    # Pack data into JSON files
    # create_export_file(json.dumps(ytd_s, indent=2), "YTD")
    # create_export_file(json.dumps(monthly_s, indent=2), "monthly_motals")
    create_export_file(json.dumps(primary_s, indent=2), "categories")
    create_export_file(json.dumps(secondary_s, indent=2), "subcategories")
