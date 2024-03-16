import json
import os
from decimal import Decimal


def decimal_to_string(decimal: Decimal) -> str:
    """Serialize Decimal type to string."""
    serialized: str
    serialized = str(decimal)
    return serialized


def serialize(
    primary: dict[str, Decimal], secondary: dict[str, dict[str, Decimal]]
) -> tuple[dict, dict]:
    """Convert data to serializable format."""
    primary_serial = {key: decimal_to_string(value) for key, value in primary.items()}

    secondary_serial = {
        key: {sub_key: decimal_to_string(value[sub_key]) for sub_key in value}
        for key, value in secondary.items()
    }

    return primary_serial, secondary_serial


def pack_json(primary: dict[str, Decimal], secondary: dict[str, dict[str, Decimal]]):
    """Pack calculated data into json object."""
    primary_json, secondary_json = serialize(primary, secondary)
    return json.dumps(primary_json, indent=3), json.dumps(secondary_json, indent=3)


def create_export_file(a, b):
    """Create JSON file and write data to it."""
    path = os.getcwd() + "/data/output/"
    name1 = "output_1.json"
    name2 = "output_2.json"

    with open(path + name1, "w") as file1:
        file1.write(a)

    with open(path + name2, "w") as file2:
        file2.write(b)


def export_to_json(a, b) -> None:
    """Serialize data, pack into JSON format, export."""
    pri, sec = pack_json(a, b)
    create_export_file(pri, sec)
