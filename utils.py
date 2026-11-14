from datetime import datetime


def get_valid_date(prompt):
    while True:
        value = input(prompt).strip()

        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format.")


def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))

            if amount < 0:
                print("Amount cannot be negative.")
                continue

            return round(amount, 2)

        except ValueError:
            print("Please enter a valid amount.")


def get_valid_id(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("ID must be greater than zero.")

        except ValueError:
            print("Please enter a valid numeric ID.")


def get_valid_category(categories):
    print("\nExpense Categories:")

    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    while True:
        try:
            choice = int(input("Select category: "))

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

            print("Invalid category choice.")

        except ValueError:
            print("Please enter a valid number.")
