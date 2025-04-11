import csv
import time


def load_actions_from_csv(file_path: str) -> list[dict[str, float]]:
    """Load actions from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list[dict[str, float]]: List of actions with name, cost, and profit.
    """
    actions = []
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cost = int(row["Coût par action (en euros)"])
                benefit = float(row["Bénéfice (après 2 ans)"].replace("%", "")) / 100
                actions.append({
                    "name": row["Actions #"],
                    "cost": cost,
                    "profit": cost * benefit
                })
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        exit(1)
    except UnicodeDecodeError:
        print("Error: File encoding issue. Trying with 'latin-1'...")
        with open(file_path, newline="", encoding="latin-1") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cost = int(row["Coût par action (en euros)"])
                benefit = float(row["Bénéfice (après 2 ans)"].replace("%", "")) / 100
                actions.append({
                    "name": row["Actions #"],
                    "cost": cost,
                    "profit": cost * benefit
                })
    return actions


def optimized_investment(actions: list[dict[str, float]], budget: int = 500) -> tuple[list[str], int, float]:
    """Find the best combination of actions using dynamic programming (1D DP).

    Args:
        actions (list[dict[str, float]]): List of actions with name, cost, and profit.
        budget (int): Maximum budget available (default: 500).

    Returns:
        tuple[list[str], int, float]: Selected action names, total cost, total profit.
    """
    # Initialize DP array and tracking for included actions
    dp = [0] * (budget + 1)
    included = [[] for _ in range(budget + 1)]

    # Process each action
    for action in actions:
        cost = action["cost"]
        profit = action["profit"]
        name = action["name"]
        # Update DP array from right to left
        for w in range(budget, cost - 1, -1):
            profit_with = dp[w - cost] + profit
            if profit_with > dp[w]:
                dp[w] = profit_with
                included[w] = included[w - cost] + [name]

    # Get the result for the full budget
    selected_names = included[budget]
    total_cost = sum(a["cost"] for a in actions if a["name"] in selected_names)
    total_profit = dp[budget]

    return selected_names, total_cost, total_profit


def main():
    """Run the dynamic programming algorithm and display the results."""
    file_path = "data/Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
    actions = load_actions_from_csv(file_path)

    print("Running dynamic programming algorithm...")
    start_time = time.time()
    selected, total_cost, total_profit = optimized_investment(actions)
    duration = time.time() - start_time

    print("\nBest combination:")
    for name in selected:
        print(f"- {name}")
    print(f"\nTotal cost: {total_cost} €")
    print(f"Total profit after 2 years: {total_profit:.2f} €")
    print(f"Execution time: {duration:.4f} seconds")


if __name__ == "__main__":
    main()