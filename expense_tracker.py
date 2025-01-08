from expense import Expense
import calendar
import datetime


def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    # Get user input for expense.
    expense = get_user_expense()

    # Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expenses.
    summarize_expenses_with_dp(expense_file_path, budget)


def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses_with_dp(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense with Budget Optimization")
    expenses: list[Expense] = []

    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if not line.strip():  # Skip empty lines
                continue

            try:
                expense_name, expense_amount, expense_category = line.strip().split(",")
                line_expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                )
                expenses.append(line_expense)
            except ValueError:
                print(f"⚠️ Skipping malformed line: {line.strip()}")

    selected_expenses, max_spending = budget_optimization_dp(expenses, budget)

    print("🛒 Selected Expenses for Optimal Budget Allocation:")
    for expense in selected_expenses:
        print(f"  {expense.category} - {expense.name}: ${expense.amount:.2f}")

    print(f"💵 Total Spending with Optimization: ${max_spending:.2f}")
    print(f"✅ Budget Remaining: ${budget - max_spending:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        daily_budget = (budget - max_spending) / remaining_days
        print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))
    else:
        print("🛑 No days remaining in the month.")


def budget_optimization_dp(expenses, budget):
    
   #Using DP here. 

    n = len(expenses)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for b in range(1, budget + 1):
            if expenses[i - 1].amount <= b:
                dp[i][b] = max(dp[i - 1][b], dp[i - 1][b - int(expenses[i - 1].amount)] + expenses[i - 1].amount)
            else:
                dp[i][b] = dp[i - 1][b]

    selected_expenses = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            selected_expenses.append(expenses[i - 1])
            b -= int(expenses[i - 1].amount)

    return selected_expenses, dp[n][budget]


def green(text):
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()
