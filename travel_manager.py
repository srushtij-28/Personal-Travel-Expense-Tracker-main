from datetime import datetime

from storage import load_trips, save_trips
from config import EXPENSE_CATEGORIES


def create_trip(destination, start_date, end_date, budget):
    trips = load_trips()

    trip_id = max(
        [trip["id"] for trip in trips],
        default=0
    ) + 1

    trip = {
        "id": trip_id,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "expenses": []
    }

    trips.append(trip)
    save_trips(trips)

    print("\nTrip created successfully!")
    print(f"Trip ID: {trip_id}")


def view_trips():
    trips = load_trips()

    if not trips:
        print("\nNo trips found.")
        return

    print("\n" + "-" * 100)
    print(
        f"{'ID':<6} {'Destination':<22} {'Start Date':<15} "
        f"{'End Date':<15} {'Budget':<15} {'Spent':<15}"
    )
    print("-" * 100)

    for trip in trips:
        total_spent = sum(
            expense["amount"] for expense in trip["expenses"]
        )

        print(
            f"{trip['id']:<6} "
            f"{trip['destination'][:21]:<22} "
            f"{trip['start_date']:<15} "
            f"{trip['end_date']:<15} "
            f"₹{trip['budget']:<14.2f} "
            f"₹{total_spent:<14.2f}"
        )

    print("-" * 100)


def get_trip_by_id(trips, trip_id):
    for trip in trips:
        if trip["id"] == trip_id:
            return trip

    return None


def add_expense(trip_id, title, category, amount, expense_date, notes):
    trips = load_trips()
    trip = get_trip_by_id(trips, trip_id)

    if not trip:
        print("\nTrip ID not found.")
        return

    expense_id = max(
        [expense["id"] for expense in trip["expenses"]],
        default=0
    ) + 1

    expense = {
        "id": expense_id,
        "title": title,
        "category": category,
        "amount": amount,
        "date": expense_date,
        "notes": notes
    }

    trip["expenses"].append(expense)
    save_trips(trips)

    print("\nExpense added successfully!")


def view_expenses(trip_id):
    trips = load_trips()
    trip = get_trip_by_id(trips, trip_id)

    if not trip:
        print("\nTrip ID not found.")
        return

    expenses = trip["expenses"]

    if not expenses:
        print("\nNo expenses recorded for this trip.")
        return

    print(f"\nExpenses for {trip['destination']}")
    print("-" * 90)
    print(
        f"{'ID':<6} {'Title':<22} {'Category':<18} "
        f"{'Date':<15} {'Amount':<15}"
    )
    print("-" * 90)

    for expense in expenses:
        print(
            f"{expense['id']:<6} "
            f"{expense['title'][:21]:<22} "
            f"{expense['category']:<18} "
            f"{expense['date']:<15} "
            f"₹{expense['amount']:<14.2f}"
        )

    print("-" * 90)

    total = sum(expense["amount"] for expense in expenses)
    print(f"Total Expenses: ₹{total:.2f}")


def search_trips(keyword):
    trips = load_trips()
    keyword = keyword.lower()

    results = [
        trip for trip in trips
        if keyword in trip["destination"].lower()
    ]

    if not results:
        print("\nNo matching trips found.")
        return

    print("\nMatching Trips:")

    for trip in results:
        total = sum(
            expense["amount"] for expense in trip["expenses"]
        )

        print(
            f"\nTrip ID: {trip['id']}"
            f"\nDestination: {trip['destination']}"
            f"\nStart Date: {trip['start_date']}"
            f"\nEnd Date: {trip['end_date']}"
            f"\nBudget: ₹{trip['budget']:.2f}"
            f"\nTotal Spent: ₹{total:.2f}"
        )


def filter_expenses_by_category(trip_id, category):
    trips = load_trips()
    trip = get_trip_by_id(trips, trip_id)

    if not trip:
        print("\nTrip ID not found.")
        return

    results = [
        expense for expense in trip["expenses"]
        if expense["category"] == category
    ]

    if not results:
        print("\nNo expenses found in this category.")
        return

    print(f"\n{category} Expenses:")

    for expense in results:
        print(
            f"ID: {expense['id']} | "
            f"{expense['title']} | "
            f"{expense['date']} | "
            f"₹{expense['amount']:.2f}"
        )

    total = sum(item["amount"] for item in results)
    print(f"\nCategory Total: ₹{total:.2f}")


def update_expense(trip_id, expense_id, title, category,
                   amount, expense_date, notes):

    trips = load_trips()
    trip = get_trip_by_id(trips, trip_id)

    if not trip:
        print("\nTrip ID not found.")
        return

    for expense in trip["expenses"]:
        if expense["id"] == expense_id:
            expense["title"] = title
            expense["category"] = category
            expense["amount"] = amount
            expense["date"] = expense_date
            expense["notes"] = notes

            save_trips(trips)
            print("\nExpense updated successfully!")
            return

    print("\nExpense ID not found.")


def delete_expense(trip_id, expense_id):
    trips = load_trips()
    trip = get_trip_by_id(trips, trip_id)

    if not trip:
        print("\nTrip ID not found.")
        return

    updated_expenses = [
        expense for expense in trip["expenses"]
        if expense["id"] != expense_id
    ]

    if len(updated_expenses) == len(trip["expenses"]):
        print("\nExpense ID not found.")
        return

    trip["expenses"] = updated_expenses
    save_trips(trips)

    print("\nExpense deleted successfully!")


def delete_trip(trip_id):
    trips = load_trips()

    updated_trips = [
        trip for trip in trips
        if trip["id"] != trip_id
    ]

    if len(updated_trips) == len(trips):
        print("\nTrip ID not found.")
        return

    save_trips(updated_trips)
    print("\nTrip and its expense records deleted successfully!")


def show_trip_statistics():
    trips = load_trips()

    if not trips:
        print("\nNo trip statistics available.")
        return

    total_trips = len(trips)
    total_budget = sum(trip["budget"] for trip in trips)

    all_expenses = [
        expense
        for trip in trips
        for expense in trip["expenses"]
    ]

    total_spent = sum(
        expense["amount"] for expense in all_expenses
    )

    remaining_budget = total_budget - total_spent

    category_totals = {}

    for expense in all_expenses:
        category = expense["category"]

        category_totals[category] = (
            category_totals.get(category, 0) + expense["amount"]
        )

    print("\n========== TRAVEL STATISTICS ==========")
    print(f"Total Trips: {total_trips}")
    print(f"Total Budget: ₹{total_budget:.2f}")
    print(f"Total Expenses: ₹{total_spent:.2f}")
    print(f"Budget Remaining: ₹{remaining_budget:.2f}")

    print("\nCategory-wise Expenses:")

    if category_totals:
        for category, amount in category_totals.items():
            print(f"{category}: ₹{amount:.2f}")
    else:
        print("No expenses recorded.")

    print("=======================================")
