# -*- coding: utf-8 -*-
"""Martin Hasson

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p71NHIWM54Iq8MOxN_Yh76xEBL-2XxY4
"""

import pandas as pd
import numpy as np

def read_transportation_problem(file_path):
    df = pd.read_excel(file_path)
    print("Dataframe contents:")
    print(df)
    sources = df['Source'].unique()
    destinations = df['Destination'].unique()
    supply = []
    cost_matrix = []
    for source in sources:
        source_data = df[df['Source'] == source]
        supply.append(source_data['Supply'].iloc[0])
        source_costs = []
        for dest in destinations:
            cost = source_data[source_data['Destination'] == dest]['Cost'].values[0]
            source_costs.append(cost)
        cost_matrix.append(source_costs)
    demand = []
    for dest in destinations:
        dest_demand = df[df['Destination'] == dest]['Demand'].iloc[0]
        demand.append(dest_demand)
    return np.array(supply), np.array(demand), np.array(cost_matrix)

def northwest_corner_rule(supply, demand):
    allocation = np.zeros((len(supply), len(demand)))
    remaining_supply = supply.copy()
    remaining_demand = demand.copy()
    i, j = 0, 0
    while i < len(remaining_supply) and j < len(remaining_demand):
        allocation_amount = min(remaining_supply[i], remaining_demand[j])
        allocation[i][j] = allocation_amount
        remaining_supply[i] -= allocation_amount
        remaining_demand[j] -= allocation_amount
        if remaining_supply[i] == 0:
            i += 1
        if remaining_demand[j] == 0:
            j += 1
    return allocation

def print_result(method_name, allocation, sources, destinations):
    print(f"\n{method_name} Solution:")
    result_df = pd.DataFrame(allocation, index=sources, columns=destinations)
    print(result_df)
    return result_df

def calculate_total_cost(allocation, cost_matrix):
    total_cost = np.sum(allocation * cost_matrix)
    print(f"\nTotal Cost: {total_cost}")
    return total_cost

def main():
    file_path = "transportation_problem.xlsx"
    try:
        supply, demand, cost = read_transportation_problem(file_path)
        sources = ['S1', 'S2', 'S3']
        destinations = ['D1', 'D2', 'D3']
        print("\nSupply:", supply)
        print("Demand:", demand)
        print("\nCost Matrix:")
        cost_df = pd.DataFrame(cost, index=sources, columns=destinations)
        print(cost_df)
        print(f"\nTotal Supply: {np.sum(supply)}")
        print(f"Total Demand: {np.sum(demand)}")
        nw_allocation = northwest_corner_rule(supply.copy(), demand.copy())
        result_df = print_result("Northwest Corner Rule", nw_allocation, sources, destinations)
        calculate_total_cost(nw_allocation, cost)
    except FileNotFoundError:
        print(f"Error: File not found at path {file_path}")
    except Exception as e:
        print("An error occurred:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()