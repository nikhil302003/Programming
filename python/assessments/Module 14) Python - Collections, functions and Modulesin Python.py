# ============================
# MediTrack - Pharmacy Console App
# QuickMed Pharmacy
# ============================

from datetime import datetime

# ----------------------------
# In-memory data storage
# ----------------------------
inventory = {
    "Paracetamol": {"price": 10.0, "stock": 100},
    "Cough Syrup": {"price": 75.0, "stock": 40},
    "Vitamin C": {"price": 5.0, "stock": 200}
}

sales = []


# ----------------------------
# Display Inventory
# ----------------------------
def view_inventory():
    print("\n========== CURRENT INVENTORY ==========")
    print(f"{'Medicine':15} {'Price':10} {'Stock':10}")
    print("-" * 40)

    for medicine, details in inventory.items():
        print(f"{medicine:15} ₹{details['price']:<9} {details['stock']:<10}")

    print("-" * 40)


# ----------------------------
# Add or Update Medicine
# ----------------------------
def add_or_update_medicine():
    try:
        name = input("\nEnter medicine name: ").strip()

        price = float(input("Enter price: "))
        stock = int(input("Enter stock quantity: "))

        if name in inventory:
            inventory[name]["price"] = price
            inventory[name]["stock"] += stock
            print("✔ Medicine updated successfully.")
        else:
            inventory[name] = {"price": price, "stock": stock}
            print("✔ Medicine added successfully.")

    except ValueError:
        print("❌ Invalid input. Please enter valid numbers.")


# ----------------------------
# Process Medicine Sale
# ----------------------------
def process_sale():
    try:
        customer = input("\nEnter customer name: ").strip()
        medicine = input("Enter medicine name: ").strip()
        quantity = int(input("Enter quantity: "))

        if medicine not in inventory:
            print("❌ Medicine not found.")
            return

        if inventory[medicine]["stock"] < quantity:
            print("❌ Insufficient stock available.")
            return

        total_price = quantity * inventory[medicine]["price"]
        inventory[medicine]["stock"] -= quantity

        sale = {
            "customer": customer,
            "medicine": medicine,
            "quantity": quantity,
            "total": total_price,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        sales.append(sale)

        print("\n========== BILL ==========")
        print(f"Customer : {customer}")
        print(f"Medicine : {medicine}")
        print(f"Quantity : {quantity}")
        print(f"Total    : ₹{total_price}")
        print(f"Date     : {sale['date']}")
        print("==========================")

    except ValueError:
        print("❌ Please enter a valid quantity.")


# ----------------------------
# View Sales History
# ----------------------------
def view_sales():
    if not sales:
        print("\nNo sales recorded yet.")
        return

    print("\n========== SALES HISTORY ==========")
    for s in sales:
        print(
            f"{s['date']} | {s['customer']} | "
            f"{s['medicine']} x{s['quantity']} | ₹{s['total']}"
        )
    print("-" * 40)


# ----------------------------
# Main Menu
# ----------------------------
def main_menu():
    while True:
        print("\n========= MediTrack Menu =========")
        print("1. View Inventory")
        print("2. Add / Update Medicine")
        print("3. Process Sale")
        print("4. View Sales History")
        print("5. Exit")
        print("=================================")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_or_update_medicine()
        elif choice == "3":
            process_sale()
        elif choice == "4":
            view_sales()
        elif choice == "5":
            print("\nThank you for using MediTrack!")
            break
        else:
            print("❌ Invalid choice. Try again.")


# ----------------------------
# Program Start
# ----------------------------
main_menu()
