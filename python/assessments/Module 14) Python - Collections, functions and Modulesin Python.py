from datetime import datetime

# Medicine data
inventory = {
    "Paracetamol": {"price": 10, "stock": 100},
    "Cough Syrup": {"price": 75, "stock": 40},
    "Vitamin C": {"price": 5, "stock": 200}
}

sales = []


def show_inventory():
    print("\n--- Inventory ---")
    print("Medicine        Price   Stock")
    print("------------------------------")
    for name in inventory:
        print(f"{name:15} {inventory[name]['price']:6} {inventory[name]['stock']:6}")


def add_medicine():
    name = input("\nMedicine name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))

        if name in inventory:
            inventory[name]["price"] = price
            inventory[name]["stock"] += stock
            print("Medicine updated.")
        else:
            inventory[name] = {"price": price, "stock": stock}
            print("Medicine added.")

    except:
        print("Wrong input.")


def sell_medicine():
    customer = input("\nCustomer name: ")
    medicine = input("Medicine name: ")

    if medicine not in inventory:
        print("Medicine not available.")
        return

    try:
        qty = int(input("Quantity: "))

        if qty > inventory[medicine]["stock"]:
            print("Not enough stock.")
            return

        total = qty * inventory[medicine]["price"]
        inventory[medicine]["stock"] -= qty

        sales.append({
            "customer": customer,
            "medicine": medicine,
            "qty": qty,
            "total": total,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M")
        })

        print("\n--- Bill ---")
        print("Customer:", customer)
        print("Medicine:", medicine)
        print("Quantity:", qty)
        print("Total: ₹", total)

    except:
        print("Invalid quantity.")


def show_sales():
    if not sales:
        print("\nNo sales yet.")
        return

    print("\n--- Sales History ---")
    for s in sales:
        print(f"{s['date']} | {s['customer']} | {s['medicine']} x{s['qty']} | ₹{s['total']}")


while True:
    print("\n1. View Inventory")
    print("2. Add Medicine")
    print("3. Sell Medicine")
    print("4. View Sales")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        show_inventory()
    elif choice == "2":
        add_medicine()
    elif choice == "3":
        sell_medicine()
    elif choice == "4":
        show_sales()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")
