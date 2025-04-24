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


def brute_force_investment(actions: list[dict[str, float]], budget: int = 500) -> tuple[list[str], int, float]:
    """Find the best combination of actions using a brute-force approach.

    Args:
        actions (list[dict[str, float]]): List of actions with name, cost, and profit.
        budget (int): Maximum budget available (default: 500).

    Returns:
        tuple[list[str], int, float]: Selected action names, total cost, total profit.
    """
    n = len(actions)
    best_profit = 0
    best_combination = []
    best_cost = 0

    # Try all 2^n combinations
    for i in range(2**n):
        current_combination = []
        current_cost = 0
        current_profit = 0

        # Check each bit to decide which actions to include
        for j in range(n):
            if i & (1 << j):
                current_combination.append(actions[j]["name"])
                current_cost += actions[j]["cost"]
                current_profit += actions[j]["profit"]

        # Update the best combination if within budget and better profit
        if current_cost <= budget and current_profit > best_profit:
            best_profit = current_profit
            best_combination = current_combination
            best_cost = current_cost

    return best_combination, best_cost, best_profit


def main():
    """Run the brute-force algorithm and display the results."""
    file_path = "data/Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
    actions = load_actions_from_csv(file_path)

    print("Running brute-force algorithm...")
    start_time = time.time()
    selected, total_cost, total_profit = brute_force_investment(actions)
    duration = time.time() - start_time

    print("\nBest combination:")
    for name in selected:
        print(f"- {name}")
    print(f"\nTotal cost: {total_cost} €")
    print(f"Total profit after 2 years: {total_profit:.2f} €")
    print(f"Execution time: {duration:.4f} seconds")


if __name__ == "__main__":
    main()