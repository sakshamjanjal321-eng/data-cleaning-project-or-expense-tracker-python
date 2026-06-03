import os
import pytest
import tempfile
from datetime import datetime
from src import expense_tracker
from src.expense_tracker import Expense, ExpenseTracker

@pytest.fixture
def temp_expense_file():
    # Create a temporary file and override the tracker's DATA_FILE path
    fd, temp_path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    
    # Save the original DATA_FILE path to restore it later
    original_data_file = expense_tracker.DATA_FILE
    expense_tracker.DATA_FILE = temp_path
    
    yield temp_path
    
    # Restore original and clean up the temp file
    expense_tracker.DATA_FILE = original_data_file
    if os.path.exists(temp_path):
        os.remove(temp_path)

def test_expense_initialization():
    exp = Expense("2026-06-04", "food", 150.50, "lunch")
    assert exp.date == "2026-06-04"
    assert exp.category == "food"
    assert exp.amount == 150.50
    assert exp.description == "lunch"
    
    dict_rep = exp.to_dict()
    assert dict_rep["date"] == "2026-06-04"
    assert dict_rep["category"] == "food"
    assert dict_rep["amount"] == 150.50
    assert dict_rep["description"] == "lunch"

def test_tracker_add_expense(temp_expense_file):
    # Ensure starting clean
    tracker = ExpenseTracker()
    assert len(tracker.expenses) == 0
    
    # Add a valid expense
    tracker.add("food", "120.00", "Snacks")
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0].category == "food"
    assert tracker.expenses[0].amount == 120.00
    assert tracker.expenses[0].description == "Snacks"
    
    # Verify it saved to disk
    new_tracker = ExpenseTracker()
    assert len(new_tracker.expenses) == 1
    assert new_tracker.expenses[0].description == "Snacks"

def test_tracker_add_invalid_category(temp_expense_file):
    tracker = ExpenseTracker()
    # Invalid category should not be added
    tracker.add("invalid_cat", "100.00", "Test")
    assert len(tracker.expenses) == 0

def test_tracker_add_invalid_amount(temp_expense_file):
    tracker = ExpenseTracker()
    # Non-numeric amount should not be added
    tracker.add("food", "not_a_number", "Test")
    assert len(tracker.expenses) == 0

def test_tracker_filter_by_month(temp_expense_file):
    tracker = ExpenseTracker()
    
    # Inject test expenses manually since add() uses current date
    tracker.expenses = [
        Expense("2026-01-15", "food", 50.0, "lunch"),
        Expense("2026-01-20", "utilities", 100.0, "power"),
        Expense("2026-02-10", "transport", 20.0, "taxi"),
    ]
    tracker.save()
    
    # Filter for Jan 2026
    jan_expenses = tracker.filter_by_month(2026, 1)
    assert len(jan_expenses) == 2
    assert jan_expenses[0].category == "food"
    assert jan_expenses[1].category == "utilities"
    
    # Filter for Feb 2026
    feb_expenses = tracker.filter_by_month(2026, 2)
    assert len(feb_expenses) == 1
    assert feb_expenses[0].category == "transport"

def test_tracker_available_months(temp_expense_file):
    tracker = ExpenseTracker()
    tracker.expenses = [
        Expense("2026-01-15", "food", 50.0, "lunch"),
        Expense("2026-03-20", "utilities", 100.0, "power"),
        Expense("2025-12-10", "transport", 20.0, "taxi"),
    ]
    
    months = tracker.get_available_months()
    assert months == [(2025, 12), (2026, 1), (2026, 3)]
