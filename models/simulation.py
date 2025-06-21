import math

def compound_growth_with_visualization(
    monthly_plan=[(1, 36, 5000)],        # [(start_month, end_month, monthly_contribution)]
    roth_ira_cap=7_000,
    roth_ira_enabled=True,
    k401_cap=23_000,
    k401_enabled=True,
    simulation_months=36,
    roth_ira_return=0.10,
    k401_return=0.10,
    dca_return=0.10,
    stock_return=0.10,
    dca_ratio=0.60,
    stock_ratio=0.40,
    inflation_rate=0.025,
    initial_roth=0,
    initial_401k=0,
    initial_dca=0,
    initial_stock=0,
):
    """
    Simulates and visualizes compound investment growth with different return rates for each investment type.
    Returns a dict of all tracked values and contributions.
    """
    # Convert annual returns to monthly returns
    roth_ira_monthly = (1 + roth_ira_return) ** (1 / 12) - 1
    k401_monthly = (1 + k401_return) ** (1 / 12) - 1
    dca_monthly = (1 + dca_return) ** (1 / 12) - 1
    stock_monthly = (1 + stock_return) ** (1 / 12) - 1
    
    timeline = [float(x) for x in range(simulation_months + 1)]

    total_value = [initial_roth + initial_401k + initial_dca + initial_stock]
    roth_ira_value = [initial_roth]
    k401_value = [initial_401k]
    self_dca_value = [initial_dca]
    self_stock_value = [initial_stock]
    
    roth_ira_contrib = 0
    k401_contrib = 0
    
    # Track total contributions over time
    total_contributions = [0]  # Start with 0 contributions
    roth_contributions = [0]
    k401_contributions = [0]
    dca_contributions = [0]
    stock_contributions = [0]
    
    for month in range(1, simulation_months + 1):
        # Determine current monthly contribution
        monthly_contribution = 0
        for start, end, amt in monthly_plan:
            if start <= month <= end:
                monthly_contribution = amt
                break

        # Allocate contributions
        roth_ira_monthly_contrib = min(monthly_contribution, roth_ira_cap / 12) if roth_ira_enabled else 0
        remaining_after_roth = monthly_contribution - roth_ira_monthly_contrib
        
        k401_monthly_contrib = min(remaining_after_roth, k401_cap / 12) if k401_enabled else 0
        remaining_after_401k = remaining_after_roth - k401_monthly_contrib
        
        dca_monthly_contrib = remaining_after_401k * dca_ratio
        stock_monthly_contrib = remaining_after_401k * stock_ratio

        # Compound growth with different returns for each investment type
        roth_ira_contrib = roth_ira_contrib * (1 + roth_ira_monthly) + roth_ira_monthly_contrib
        k401_contrib = k401_contrib * (1 + k401_monthly) + k401_monthly_contrib
        dca_total = self_dca_value[-1] * (1 + dca_monthly) + dca_monthly_contrib
        stock_total = self_stock_value[-1] * (1 + stock_monthly) + stock_monthly_contrib

        roth_ira_value.append(roth_ira_contrib)
        k401_value.append(k401_contrib)
        self_dca_value.append(dca_total)
        self_stock_value.append(stock_total)
        
        total_value.append(roth_ira_contrib + k401_contrib + dca_total + stock_total)

        # Track cumulative contributions
        total_contributions.append(total_contributions[-1] + monthly_contribution)
        roth_contributions.append(roth_contributions[-1] + roth_ira_monthly_contrib)
        k401_contributions.append(k401_contributions[-1] + k401_monthly_contrib)
        dca_contributions.append(dca_contributions[-1] + dca_monthly_contrib)
        stock_contributions.append(stock_contributions[-1] + stock_monthly_contrib)

    # Ensure all data is in standard Python types
    timeline = list(range(simulation_months + 1))
    total_value = [float(x) for x in total_value]
    roth_ira_value = [float(x) for x in roth_ira_value]
    k401_value = [float(x) for x in k401_value]
    dca_value = [float(x) for x in self_dca_value]
    stock_value = [float(x) for x in self_stock_value]
    total_contributions = [float(x) for x in total_contributions]
    roth_contributions = [float(x) for x in roth_contributions]
    k401_contributions = [float(x) for x in k401_contributions]
    dca_contributions = [float(x) for x in dca_contributions]
    stock_contributions = [float(x) for x in stock_contributions]

    # Calculate inflation-adjusted values
    inflation_monthly = (1 + inflation_rate) ** (1 / 12) - 1
    inflation_adjustment = [(1 + inflation_monthly) ** month for month in timeline]
    
    total_adjusted = [total_value[i] / inflation_adjustment[i] for i in range(len(total_value))]
    roth_adjusted = [roth_ira_value[i] / inflation_adjustment[i] for i in range(len(roth_ira_value))]
    k401_adjusted = [k401_value[i] / inflation_adjustment[i] for i in range(len(k401_value))]
    dca_adjusted = [dca_value[i] / inflation_adjustment[i] for i in range(len(dca_value))]
    stock_adjusted = [stock_value[i] / inflation_adjustment[i] for i in range(len(stock_value))]

    return {
        "Month": timeline,
        "Total": total_value,
        "Roth IRA": roth_ira_value,
        "401(k)": k401_value,
        "ETF DCA": dca_value,
        "Stock Picks": stock_value,
        "Total_Adjusted": total_adjusted,
        "Roth IRA_Adjusted": roth_adjusted,
        "401(k)_Adjusted": k401_adjusted,
        "ETF DCA_Adjusted": dca_adjusted,
        "Stock Picks_Adjusted": stock_adjusted,
        "Total_Contributions": total_contributions,
        "Roth_Contributions": roth_contributions,
        "401k_Contributions": k401_contributions,
        "DCA_Contributions": dca_contributions,
        "Stock_Contributions": stock_contributions,
    } 