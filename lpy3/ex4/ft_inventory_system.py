import sys

def main():
    raw_args = sys.argv[1:]
    if not raw_args:
        print("Usage: python3 ft_inventory_system.py item:qty item:qty ...")
        return

    inv = dict()
    try:
        for arg in raw_args:
            key, value = arg.split(":")
            inv.update({key: int(value)})
    except ValueError as e:
        print(f"Error: invalid input - type: {type(e).__name__}, type: {e.args}")
# eっていうインスタンスのクラス名の名前
    
    print("=== Inventory System Analysis ===")
    total_value = sum(inv.values())
    print(f"Total items in inventory: {total_value}")
    print(f"Unique item types: {len(inv)}")
    print()

    print("== Current Inventory ===")
    for key, value in inv.items():
        per = (value / total_value) * 100
        print(f"{key}: {value} units {per:.1f}%")
    print()
# for key, value in inv:
#    print(f"{key}, {value}")invにするとkeyだけみる

    print("=== Inventory Statistics ===")
    most_value = 0
    most_key = ""
    least_value = float('inf')
    least_key = ""
    for key, value in inv.items():
        if value > most_value:
            most_value = value
            most_key = key
        if value < least_value:
            least_value = value
            least_key = key
    print(f"Most abundant: {most_key} ({most_value} units)")
    print(f"Least abundant: {least_key} ({least_value} unit)")
    print()

    categories = {"moderate": dict(), "scarce": dict()}
    restock = []
    print("=== Item Categories ===")
    for key, value in inv.items():
        if value >= 5:
            categories["moderate"].update({key: value})
        else:
            categories["scarce"].update({key: value})
        if value <= 1:
            restock.append({key: value})
    print(f"Moderate: {categories.get('moderate')}")
    print(f"Scarce: {categories.get('scarce')}")
    print()

    print("=== Management Suggestions ===")
    print(f"Restock needed: {restock}")
    print()

    print("== Dictionary Properties Demo ===")
    print(f"Dictionary keys: {inv.keys()}")



main()