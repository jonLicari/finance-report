from decimal import Decimal
import json


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

    # Pack JSON with data
    primary_json, secondary_json = serialize(primary, secondary)
    print(primary_json, secondary_json)
    return json.dumps(primary_json), json.dumps(secondary_json)


def export_to_json(a, b) -> None:
    """Serialize data, pack into JSON format, export."""
    pack_json(a, b)
