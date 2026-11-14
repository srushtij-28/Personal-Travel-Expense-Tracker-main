from datetime import date

from storage import initialize_storage

from config import EXPENSE_CATEGORIES

from travel_manager import (
    create_trip,
    view_trips,
    add_expense,
    view_expenses,
    search_trips,
    filter_expenses_by_category,
    update_expense,
    delete_expense,
    delete_trip,
    show_trip_statistics
)

from utils import (
    get_valid_date,
    get_valid_amount,
    get_valid_id,
    get_valid_category
)


def display_menu():
    print("\n========== PERSONAL TRAVEL EXPENSE TRACKER ==========")
    print("1. Create Trip")
    print("2. View All Trips")
    print("3. Search Trip")
    print("4. Add Trip Expense")
    print("5. View Trip Expenses")
    print("6. Filter Expenses by Category")
    print("7. Update Expense")
    print("8. Delete Expense")
    print("9. Delete Trip")
    print("10. Travel Statistics")
    print("11. Exit")
    print("=====================================================")


def get_trip_details():
    destination = input("Enter destination: ").strip()

    start_date = get_valid_date(
        "Enter start date (YYYY-MM-DD): "
    )

    end_date = get_valid_date(
        "Enter end date (YYYY-MM-DD): "
    )

    if end_date < start_date:
        print("End date cannot be before start date.")
        return None

    budget = get_valid_amount("Enter trip budget (₹): ")

    if not destination:
        print("Destination cannot be empty.")
        return None

    return destination, start_date, end_date, budget


def get_expense_details():
    title = input("Enter expense title: ").strip()

    category = get_valid_category(EXPENSE_CATEGORIES)

    amount = get_valid_amount("Enter expense amount (₹): ")

    expense_date = get_valid_date(
        "Enter expense date (YYYY-MM-DD): "
    )

    notes = input("Enter notes: ").strip()

    if not title:
        print("Expense title cannot be empty.")
        return None

    return title, category, amount, expense_date, notes


def main():
    initialize_storage()

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            details = get_trip_details()

            if details:
                create_trip(*details)

        elif choice == "2":
            view_trips()

        elif choice == "3":
            keyword = input("Enter destination: ").strip()
            search_trips(keyword)

        elif choice == "4":
            trip_id = get_valid_id("Enter trip ID: ")

            details = get_expense_details()

            if details:
                add_expense(trip_id, *details)

        elif choice == "5":
            trip_id = get_valid_id("Enter trip ID: ")
            view_expenses(trip_id)

        elif choice == "6":
            trip_id = get_valid_id("Enter trip ID: ")

            category = get_valid_category(EXPENSE_CATEGORIES)

            filter_expenses_by_category(trip_id, category)

        elif choice == "7":
            trip_id = get_valid_id("Enter trip ID: ")
            expense_id = get_valid_id("Enter expense ID: ")

            details = get_expense_details()

            if details:
                update_expense(trip_id, expense_id, *details)

        elif choice == "8":
            trip_id = get_valid_id("Enter trip ID: ")
            expense_id = get_valid_id("Enter expense ID: ")

            delete_expense(trip_id, expense_id)

        elif choice == "9":
            trip_id = get_valid_id("Enter trip ID: ")
            delete_trip(trip_id)

        elif choice == "10":
            show_trip_statistics()

        elif choice == "11":
            print("Thank you for using Travel Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
