import argparse
import csv
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

@dataclass
class Column:
    name: str
    column_type: str

@dataclass
class TableDefinition:
    name: str
    columns: list[Column]


def fake_city(rng: random.Random) -> str:
    return rng.choice(
        [
            "Helsinki",
            "Tampere",
            "Stockholm",
            "Berlin",
            "London",
            "Austin",
            "Tokyo",
            "Singapore",
        ]
    )


def fake_complaint(rng: random.Random) -> str:
    return rng.choice(
        [
            "Headache",
            "Burning sensation",
            "Flu-like symptoms",
            "Skin rash",
            "Pinkeye",
        ]
    )


def fake_allergy(rng: random.Random) -> str:
    return rng.choice(
        [
            "None",
            "Peanuts",
            "Pollen",
            "Lactose",
            "Penicillin",
            "Dust",
            "Shellfish",
            "Latex",
            "Onions",
            "Gluten",
        ]
    )


def infer_value(
    column_name: str,
    column_type: str,
    row_index: int,
    rng: random.Random,
) -> str | int:
    lower_name = column_name.lower()
    lower_type = column_type.lower()

    if "serial" in lower_type:
        return row_index + 1

    if "integer" in lower_type or "int" in lower_type:
        if "age" in lower_name:
            return rng.randint(16, 85)
        if "rating" in lower_name:
            return rng.randint(1, 5)
        return rng.randint(1, 10_000)

    if "timestamp" in lower_type or "date" in lower_type:
        base = datetime(2025, 1, 1, 9, 0, 0) + timedelta(hours=row_index * 3)
        return base.isoformat(sep=" ")

    if "bookingtime" in lower_name:
        base = datetime(2025, 1, 1, 9, 0, 0) + timedelta(hours=row_index * 2)
        return base.isoformat(sep=" ")
    if "full_name" in lower_name:
        return f"User {row_index + 1}"
    if "city" in lower_name:
        return fake_city(rng)
    if "gender" in lower_name:
        return rng.choice(["male", "female", "other"])
    if "email" in lower_name:
        return f"user{row_index + 1}@example.com"
    if "phone" in lower_name:
        return f"+35840{rng.randint(100000, 999999)}"
    if "complaint" in lower_name:
        return fake_complaint(rng)
    if "allergy" in lower_name:
        return fake_allergy(rng)

    if "text" in lower_type:
        return f"{column_name}_{row_index + 1}"
    if "character varying" in lower_type or "varchar" in lower_type:
        return f"{column_name}_{row_index + 1}"

    return f"value_{row_index + 1}"


def write_csv(table: TableDefinition, rows: int, output_dir: Path, seed: int) -> Path:
    rng = random.Random(f"{seed}:{table.name}")
    output_path = output_dir / f"{table.name}.csv"

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        headers = [column.name for column in table.columns]
        writer.writerow(headers)

        for i in range(rows):
            writer.writerow(
                [
                    infer_value(column.name, column.column_type, i, rng)
                    for column in table.columns
                ]
            )

    return output_path


def main(table_list: list[TableDefinition]) -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic CSV files for merkle encryption."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("generated_table_data"),
        help="Directory where CSV files will be written.",
    )
    parser.add_argument(
        "--rows-per-table",
        type=int,
        default=50,
        help="Number of synthetic rows to generate for each table.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for repeatable outputs.",
    )
    args = parser.parse_args()

    if args.rows_per_table < 1:
        raise ValueError("--rows-per-table must be at least 1.")
    
    if table_list is None or len(table_list) == 0:
        raise ValueError("No table definitions provided.")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    for table in tables:
        path = write_csv(table, args.rows_per_table, args.output_dir, args.seed)
        print(f"Wrote {path}")


if __name__ == "__main__":
    tables = [
        TableDefinition(
            name="users",
            columns=[
                Column(name="id", column_type="SERIAL PRIMARY KEY"),
                Column(name="user_full_name", column_type="TEXT"),
                Column(name="city", column_type="TEXT"),
                Column(name="gender", column_type="TEXT"),
                Column(name="age", column_type="INTEGER"),
                Column(name="email", column_type="TEXT"),
                Column(name="phone", column_type="TEXT"),
                Column(name="bookingtime", column_type="TIMESTAMP"),
                Column(name="complaint", column_type="TEXT"),
                Column(name="satisfaction_rating", column_type="INTEGER"),
                Column(name="allergy", column_type="TEXT"),
            ],
        )
    ]
    main(table_list=tables)