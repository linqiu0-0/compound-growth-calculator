import streamlit as st
from utils.irr import calculate_irr

def display_results(data, sim_years, sim_months, inflation_rate):
    st.header("📊 Results")
    
    tab1, tab2 = st.tabs(["💰 Nominal Values", "📈 Inflation-Adjusted Values"])
    
    with tab1:
        final_total = data["Total"][-1]
        initial_total = data["Total"][0]
        total_contributions = data["Total_Contributions"][-1]
        total_invested = initial_total + total_contributions
        growth = final_total - total_invested
        pct = (growth / total_invested) * 100 if total_invested > 0 else 0
        
        cash_flows = [-initial_total]
        for i in range(1, len(data["Month"])):
            monthly_contrib = data["Total_Contributions"][i] - data["Total_Contributions"][i - 1]
            cash_flows.append(-monthly_contrib)
        cash_flows.append(final_total)
        irr = calculate_irr(cash_flows) * 100
        
        cagr = ((final_total / total_invested) ** (1 / sim_years) - 1) * 100 if total_invested > 0 else 0.0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Final Portfolio", f"${final_total:,.0f}")
        col2.metric("Total Invested", f"${total_invested:,.0f}")
        col3.metric("Investment Gains", f"${growth:,.0f}")
        col4.metric("Total Return", f"{pct:.1f}%")

        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Years Simulated", sim_years)
        col6.metric("IRR (内部收益率)", f"{irr:.1f}%")
        col7.metric("CAGR (年化收益率)", f"{cagr:.1f}%")
        col8.metric("Inflation Rate", f"{inflation_rate * 100:.1f}%")
        
    with tab2:
        final_total_adj = data["Total_Adjusted"][-1]
        initial_total_adj = data["Total_Adjusted"][0]
        inflation_monthly = (1 + inflation_rate) ** (1 / 12) - 1
        inflation_adjustment_final = (1 + inflation_monthly) ** sim_months
        total_contributions_adj = total_contributions / inflation_adjustment_final
        total_invested_adj = initial_total_adj + total_contributions_adj
        growth_adj = final_total_adj - total_invested_adj
        pct_adj = (growth_adj / total_invested_adj) * 100 if total_invested_adj > 0 else 0
        
        cash_flows_adj = [-initial_total_adj]
        for i in range(1, len(data["Month"])):
            monthly_contrib_adj = (data["Total_Contributions"][i] - data["Total_Contributions"][i - 1]) / ((1 + inflation_monthly) ** i)
            cash_flows_adj.append(-monthly_contrib_adj)
        cash_flows_adj.append(final_total_adj)
        irr_adj = calculate_irr(cash_flows_adj) * 100

        # ✅ Correct way to compute real CAGR from nominal CAGR and inflation:
        real_cagr = ((1 + cagr / 100) / (1 + inflation_rate) - 1) * 100

        col9, col10, col11, col12 = st.columns(4)
        col9.metric("Final Portfolio (Real)", f"${final_total_adj:,.0f}")
        col10.metric("Total Invested (Real)", f"${total_invested_adj:,.0f}")
        col11.metric("Investment Gains (Real)", f"${growth_adj:,.0f}")
        col12.metric("Total Return (Real)", f"{pct_adj:.1f}%")
        
        col13, col14, col15, col16 = st.columns(4)
        col13.metric("Years Simulated", sim_years)
        col14.metric("IRR (内部收益率) (Real)", f"{irr_adj:.1f}%")
        col15.metric("CAGR (年化收益率) (Real)", f"{real_cagr:.1f}%")
        col16.metric("Inflation Rate", f"{inflation_rate * 100:.1f}%")
