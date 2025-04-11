# bruteforce.py

import csv
import asyncio
from concurrent.futures import ProcessPoolExecutor
import math

# Step 1: Load actions from the CSV file
def load_actions_from_csv(file_path):
    actions = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            print("CSV Headers:", reader.fieldnames)
            for row in reader:
                name = row["Actions #"]
                cost = int(row["Coût par action (en euros)"])
                benefit = float(row["Bénéfice (après 2 ans)"].replace('%', '')) / 100
                profit = cost * benefit
                actions.append({"name": name, "cost": cost, "profit": profit})
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        exit(1)
    return actions

# Step 2: Function to process a chunk of combinations (to be run in parallel)
def process_chunk(actions, start, end, budget=500):
    n = len(actions)
    max_profit = 0
    best_combination = []
    best_cost = 0
    combinations_processed = 0  # Counter for combinations

    for i in range(start, end):
        current_combination = []
        current_cost = 0
        current_profit = 0

        for j in range(n):
            if i & (1 << j):
                current_combination.append(actions[j]["name"])
                current_cost += actions[j]["cost"]
                current_profit += actions[j]["profit"]

        if current_cost <= budget and current_profit > max_profit:
            max_profit = current_profit
            best_combination = current_combination
            best_cost = current_cost

        combinations_processed += 1  # Increment the counter

    return best_combination, best_cost, max_profit, combinations_processed

# Step 3: Asynchronous brute-force algorithm
async def async_brute_force_investment(actions, budget=500, num_processes=4):
    n = len(actions)
    total_combinations = 2**n
    chunk_size = total_combinations // num_processes

    tasks = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        loop = asyncio.get_event_loop()
        for i in range(num_processes):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < num_processes - 1 else total_combinations
            print(f"Chunk {i}: Processing combinations {start} to {end-1}")
            task = loop.run_in_executor(executor, process_chunk, actions, start, end, budget)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

    max_profit = 0
    best_combination = []
    best_cost = 0
    total_combinations_processed = 0

    for combination, cost, profit, combos in results:
        if profit > max_profit:
            max_profit = profit
            best_combination = combination
            best_cost = cost
        total_combinations_processed += combos

    print(f"Total combinations processed: {total_combinations_processed}")
    print(f"Expected combinations: {total_combinations}")
    assert total_combinations_processed == total_combinations, "Not all combinations were processed!"

    return best_combination, best_cost, max_profit

# Step 4: Main function to run the program
async def main():
    file_path = "data/Liste+d'actions+-+P7+Python+-+Feuille+1.csv"
    actions = load_actions_from_csv(file_path)
    best_actions, total_cost, total_profit = await async_brute_force_investment(actions)

    print("Meilleure combinaison d'actions :")
    for action in best_actions:
        print(f"- {action}")
    print(f"Coût total : {total_cost} euros")
    print(f"Profit total après 2 ans : {total_profit:.2f} euros")

# Step 5: Run the program
if __name__ == "__main__":
    asyncio.run(main())