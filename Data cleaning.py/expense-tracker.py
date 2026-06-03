import csv
import os
from datetime import datetime

DATA_FILE = "expenses.csv"
CATEGORIES = ["food", "transport", "utilities", "entertainment", "other"]

class Expense:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = float(amount)
        self.description = description

    def to_dict(self):
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.load()

    def load(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.expenses.append(
                    Expense(row["date"], row["category"],
                            row["amount"], row["description"])
                )

    def save(self):
        with open(DATA_FILE, "w", newline="") as f:
            fieldnames = ["date", "category", "amount", "description"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for e in self.expenses:
                writer.writerow(e.to_dict())

    def add(self, category, amount, description):
        if category not in CATEGORIES:
            print(f"Invalid category. Choose from: {', '.join(CATEGORIES)}")
            return
        try:
            amount = float(amount)
        except ValueError:
            print("Amount must be a number.")
            return
        date = datetime.now().strftime("%Y-%m-%d")
        self.expenses.append(Expense(date, category, amount, description))
        self.save()
        print(f"Added: {category} - Rs.{amount:.2f} ({description})")

    # ── NEW: filter helper ───────────────────────────────────────────────────
    def filter_by_month(self, year: int, month: int):
        """Return expenses matching the given year and month."""
        return [
            e for e in self.expenses
            if e.date.startswith(f"{year}-{month:02d}")
        ]

    def get_available_months(self):
        """Return a sorted list of (year, month) tuples present in data."""
        months = set()
        for e in self.expenses:
            try:
                dt = datetime.strptime(e.date, "%Y-%m-%d")
                months.add((dt.year, dt.month))
            except ValueError:
                pass
        return sorted(months)
    # ────────────────────────────────────────────────────────────────────────

    def summary(self, expenses=None):
        """Print a summary. Pass a filtered list or leave blank for all."""
        if expenses is None:
            expenses = self.expenses
        if not expenses:
            print("No expenses found for that period.")
            return
        total = sum(e.amount for e in expenses)
        by_cat = {}
        for e in expenses:
            by_cat[e.category] = by_cat.get(e.category, 0) + e.amount
        print(f"\n{'='*35}")
        print(f"  Total spent: Rs.{total:.2f}")
        print(f"{'='*35}")
        for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
            pct = (amt / total) * 100
            print(f"  {cat:<15} Rs.{amt:>8.2f}  ({pct:.1f}%)")
        print(f"{'='*35}\n")

    def list_recent(self, n=10, expenses=None):
        """List recent entries. Pass a filtered list or leave blank for all."""
        if expenses is None:
            expenses = self.expenses
        if not expenses:
            print("No expenses found for that period.")
            return
        recent = expenses[-n:]
        print(f"\n{'Date':<12}{'Category':<15}{'Amount':>10}  Description")
        print("-" * 55)
        for e in reversed(recent):
            print(f"{e.date:<12}{e.category:<15}Rs.{e.amount:>8.2f}  {e.description}")
        print()

    # ── NEW: month filter menu ───────────────────────────────────────────────
    def filter_menu(self):
        """Let the user pick a month and show filtered summary + list."""
        months = self.get_available_months()
        if not months:
            print("No expenses recorded yet.")
            return

        print("\nAvailable months:")
        for i, (y, m) in enumerate(months, 1):
            label = datetime(y, m, 1).strftime("%B %Y")
            count = len(self.filter_by_month(y, m))
            print(f"  {i}. {label}  ({count} expense{'s' if count!=1 else ''})")

        choice = input("Choose a month number (or press Enter to cancel): ").strip()
        if not choice:
            return
        try:
            idx = int(choice) - 1
            if not (0 <= idx < len(months)):
                raise ValueError
        except ValueError:
            print("Invalid choice.")
            return

        year, month = months[idx]
        label = datetime(year, month, 1).strftime("%B %Y")
        filtered = self.filter_by_month(year, month)

        print(f"\n── {label} ──")
        self.list_recent(expenses=filtered, n=len(filtered))
        self.summary(expenses=filtered)
    # ────────────────────────────────────────────────────────────────────────


def main():
    tracker = ExpenseTracker()
    while True:
        print("\n1. Add expense")
        print("2. View summary (all time)")
        print("3. List recent (all time)")
        print("4. Filter by month")          # ← NEW menu item
        print("5. Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            cat = input(f"Category ({', '.join(CATEGORIES)}): ").strip().lower()
            amt = input("Amount (Rs.): ").strip()
            desc = input("Description: ").strip()
            tracker.add(cat, amt, desc)
        elif choice == "2":
            tracker.summary()
        elif choice == "3":
            tracker.list_recent()
        elif choice == "4":
            tracker.filter_menu()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()