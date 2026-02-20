import json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from tqdm import tqdm

# ======== CONFIGURE FILE PATH HERE ========
INPUT_FILE = Path("products.json")
OUTPUT_FILE = Path("products_with_aggregations.json")
# ===========================================


def calculate_aggregations(products):
    category_data = defaultdict(lambda: {
        "count": 0,
        "inventoryValue": Decimal("0.00")
    })

    print("Calculating aggregations...\n")

    for product in tqdm(products, desc="Processing products"):
        category = product["category"]
        price = Decimal(str(product["price"]))
        stock = Decimal(str(product["stock"]))

        category_data[category]["count"] += 1
        category_data[category]["inventoryValue"] += price * stock

    # Round values properly to 2 decimal places
    final_aggregations = {}
    for category, data in category_data.items():
        final_aggregations[category] = {
            "count": data["count"],
            "inventoryValue": float(
                data["inventoryValue"].quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            )
        }

    return final_aggregations


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"{INPUT_FILE} not found.")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])

    aggregations = calculate_aggregations(products)

    data["aggregations"] = aggregations

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("\nAggregation complete!")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()