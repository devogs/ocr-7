import csv
import time


def load_actions_from_csv(file_path: str) -> list[dict[str, float]]:
    """Load actions from a CSV file formatted with 'name', 'price', 'profit'.

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
                try:
                    cost = float(row["price"])
                    profit_percentage = float(row["profit"])
                    if cost > 0 and profit_percentage > 0:
                        actions.append({
                            "name": row["name"],
                            "cost": int(cost * 100),
                            "profit_percentage": profit_percentage,
                            "profit": (cost * profit_percentage) / 100
                        })
                except ValueError:
                    continue
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        exit(1)
    except UnicodeDecodeError:
        print("Error: Encoding issue. Please check file encoding.")
        exit(1)

    return actions


def optimized_investment(actions: list[dict[str, float]], budget: int = 500) -> tuple[list[str], float, float]:
    """Find the best combination of actions using dynamic programming (1D DP).

    Args:
        actions (list[dict[str, float]]): List of actions with name, cost, and profit.
        budget (int): Maximum budget available in € (default: 500).

    Returns:
        tuple[list[str], float, float]: Selected action names, total cost, total profit.
    """
    budget_cents = int(budget * 100)
    dp = [0.0] * (budget_cents + 1)
    included = [[] for _ in range(budget_cents + 1)]

    for action in actions:
        cost_cents = action["cost"]
        profit_euros = action["profit"]
        name = action["name"]
        for w in range(budget_cents, cost_cents - 1, -1):
            profit_with = dp[w - cost_cents] + profit_euros
            if profit_with > dp[w]:
                dp[w] = profit_with
                included[w] = included[w - cost_cents] + [name]

    selected_names = included[budget_cents]
    total_cost = sum(a["cost"] / 100 for a in actions if a["name"] in selected_names)
    total_profit = dp[budget_cents]

    return selected_names, total_cost, total_profit


def main():
    """Run the dynamic programming algorithm and display the results for both datasets."""
    datasets = ["./data/dataset1_Python+P7.csv", "./data/dataset2_Python+P7.csv"]

    for dataset in datasets:
        print(f"\n=== Processing {dataset} ===")
        actions = load_actions_from_csv(dataset)

        print("Running dynamic programming algorithm...")
        start_time = time.time()
        selected, total_cost, total_profit = optimized_investment(actions)
        duration = time.time() - start_time

        print("\nBest combination:")
        for name in selected:
            print(f"- {name}")
        print(f"\nTotal cost: {total_cost:.2f} €")
        print(f"Profit: {total_profit:.2f} €")  # Changed label to match Sienna's output
        print(f"Execution time: {duration:.4f} seconds")


if __name__ == "__main__":
    main()