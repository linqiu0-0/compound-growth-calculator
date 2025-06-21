import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

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
    
    roth_accum = initial_roth
    k401_accum = initial_401k
    
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

    # Ensure all data is in standard Python types
    timeline = list(range(simulation_months + 1))
    total_value = [float(x) for x in total_value]
    roth_ira_value = [float(x) for x in roth_ira_value]
    k401_value = [float(x) for x in k401_value]
    dca_value = [float(x) for x in self_dca_value]
    stock_value = [float(x) for x in self_stock_value]

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
    }

# -----------------------------------------------------------
# 🖼  Page config — run only once per session
# -----------------------------------------------------------
if "PAGE_CONFIG_SET" not in st.session_state:
    st.set_page_config(page_title="Investment Calculator", layout="wide")
    st.session_state.PAGE_CONFIG_SET = True

# -----------------------------------------------------------
# 📦  Heavy imports – cached so they're imported once
# -----------------------------------------------------------
@st.cache_resource
def _load_libs():
    import matplotlib.pyplot as plt
    import altair as alt
    return plt, alt

plt, alt = _load_libs()

# -----------------------------------------------------------
# 📈  Core simulation logic (unchanged)
# -----------------------------------------------------------
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
    # Convert annual return → monthly
    r_m = (1 + roth_ira_return) ** (1 / 12) - 1
    k_m = (1 + k401_return) ** (1 / 12) - 1
    d_m = (1 + dca_return) ** (1 / 12) - 1
    s_m = (1 + stock_return) ** (1 / 12) - 1

    timeline      = list(range(simulation_months + 1))
    total_value   = [initial_roth + initial_401k + initial_dca + initial_stock]
    roth_value    = [initial_roth]
    k401_value    = [initial_401k]
    dca_value     = [initial_dca]
    stock_value   = [initial_stock]

    roth_accum = initial_roth
    k401_accum = initial_401k

    for m in range(1, simulation_months + 1):
        # Which monthly contribution applies?
        contrib = next((amt for start, end, amt in monthly_plan if start <= m <= end), 0)

        # Split into account buckets
        roth_contrib  = min(contrib, roth_ira_cap / 12) if roth_ira_enabled else 0
        remain_after_roth = contrib - roth_contrib

        k401_contrib  = min(remain_after_roth, k401_cap / 12) if k401_enabled else 0
        remain        = remain_after_roth - k401_contrib

        dca_contrib   = remain * dca_ratio
        stock_contrib = remain * stock_ratio

        # Compound each bucket
        roth_accum  = roth_accum  * (1 + r_m) + roth_contrib
        k401_accum  = k401_accum  * (1 + k_m) + k401_contrib
        dca_next    = dca_value[-1]   * (1 + d_m) + dca_contrib
        stock_next  = stock_value[-1] * (1 + s_m) + stock_contrib

        # Save series
        roth_value.append(roth_accum)
        k401_value.append(k401_accum)
        dca_value.append(dca_next)
        stock_value.append(stock_next)
        total_value.append(roth_accum + k401_accum + dca_next + stock_next)

    # Ensure all data is in standard Python types
    timeline = list(range(simulation_months + 1))
    total_value = [float(x) for x in total_value]
    roth_value = [float(x) for x in roth_value]
    k401_value = [float(x) for x in k401_value]
    dca_value = [float(x) for x in dca_value]
    stock_value = [float(x) for x in stock_value]

    # Calculate inflation-adjusted values
    inflation_monthly = (1 + inflation_rate) ** (1 / 12) - 1
    inflation_adjustment = [(1 + inflation_monthly) ** month for month in timeline]
    
    total_adjusted = [total_value[i] / inflation_adjustment[i] for i in range(len(total_value))]
    roth_adjusted = [roth_value[i] / inflation_adjustment[i] for i in range(len(roth_value))]
    k401_adjusted = [k401_value[i] / inflation_adjustment[i] for i in range(len(k401_value))]
    dca_adjusted = [dca_value[i] / inflation_adjustment[i] for i in range(len(dca_value))]
    stock_adjusted = [stock_value[i] / inflation_adjustment[i] for i in range(len(stock_value))]

    return {
        "Month": timeline,
        "Total": total_value,
        "Roth IRA": roth_value,
        "401(k)": k401_value,
        "ETF DCA": dca_value,
        "Stock Picks": stock_value,
        "Total_Adjusted": total_adjusted,
        "Roth IRA_Adjusted": roth_adjusted,
        "401(k)_Adjusted": k401_adjusted,
        "ETF DCA_Adjusted": dca_adjusted,
        "Stock Picks_Adjusted": stock_adjusted,
    }

# -----------------------------------------------------------
# 🏎  Cached wrapper so the sim runs only when inputs change
# -----------------------------------------------------------
@st.cache_data(show_spinner="Running simulation…")
def run_sim(**kwargs):
    return compound_growth_with_visualization(**kwargs)

# -----------------------------------------------------------
# 🎛  Interactive UI
# -----------------------------------------------------------
def main():
    st.title("💰 Interactive Investment Calculator")
    st.markdown("---")

    # ---------- Sidebar controls ----------
    with st.sidebar:
        st.header("🏦 Initial Account Balances")
        initial_roth = st.number_input(
            "Initial Roth IRA Balance ($)", 0, step=1_000, value=0, key="main_initial_roth"
        )
        initial_401k = st.number_input(
            "Initial 401(k) Balance ($)", 0, step=1_000, value=0, key="main_initial_401k"
        )
        initial_dca = st.number_input(
            "Initial ETF DCA Balance ($)", 0, step=1_000, value=0, key="main_initial_dca"
        )
        initial_stock = st.number_input(
            "Initial Stock Picks Balance ($)", 0, step=1_000, value=0, key="main_initial_stock"
        )

        sim_years = st.slider("Simulation Duration (Years)", 1, 30, 3, key="main_sim_years")
        sim_months = sim_years * 12

        st.markdown("---"); st.header("📈 Return Rates")
        roth_r  = st.slider("Roth IRA Annual Return (%)",   0.0, 30.0, 10.0, 0.5, key="main_roth_r") / 100
        k401_r  = st.slider("401(k) Annual Return (%)",     0.0, 30.0, 10.0, 0.5, key="main_k401_r") / 100
        dca_r   = st.slider("ETF DCA Annual Return (%)",    0.0, 30.0, 10.0, 0.5, key="main_dca_r") / 100
        stock_r = st.slider("Stock Picks Annual Return (%)",0.0, 30.0, 12.0, 0.5, key="main_stock_r") / 100

        st.markdown("---"); st.header("💼 Investment Limits")
        enable_roth = st.checkbox("Enable Roth IRA", True, key="main_enable_roth_checkbox")
        roth_cap = st.number_input(
            "Roth IRA Annual Limit ($)", 0, value=7_000, step=500, disabled=not enable_roth, key="main_roth_cap"
        )

        enable_k401 = st.checkbox("Enable 401(k)", True, key="main_enable_k401_checkbox")
        k401_cap = st.number_input(
            "401(k) Annual Limit ($)", 0, value=23_000, step=1_000, disabled=not enable_k401, key="main_k401_cap"
        )

        st.markdown("---"); st.header("📊 Allocation Strategy")
        dca_ratio = st.slider("ETF DCA Allocation (%)", 0, 100, 60, 5, key="main_dca_ratio") / 100
        stock_ratio = 1 - dca_ratio
        st.write(f"**Current Allocation:** ETF DCA: {dca_ratio*100:.0f}% | Stock Picks: {stock_ratio*100:.0f}%")

        st.markdown("---"); st.header("💰 Inflation Settings")
        inflation_rate = st.slider("Annual Inflation Rate (%)", 0.0, 10.0, 2.5, 0.1, key="main_inflation_rate") / 100

    # ---------- Period configuration ----------
    st.header("📅 Investment Periods")

    # Initialize session state for periods if not exists
    if "investment_periods" not in st.session_state:
        st.session_state.investment_periods = [(1, 3, 5_000), (4, 10, 7_000), (11, 20, 10_000)]

    # Display existing periods
    st.subheader("Current Investment Periods")
    
    # Create columns for period management
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("**Periods:**")
        for i, (start, end, amt) in enumerate(st.session_state.investment_periods):
            st.write(f"Period {i+1}: Year {start} to Year {end} - ${amt:,.0f}/month")
    
    with col2:
        if st.button("➕ Add Period", key="add_period"):
            st.session_state.investment_periods.append((1, 1, 1000))
            st.rerun()
    
    # Period editing interface
    st.subheader("Edit Periods")
    
    periods_to_remove = []
    for i, (start, end, amt) in enumerate(st.session_state.investment_periods):
        with st.expander(f"Period {i+1}: Year {start} to Year {end} - ${amt:,.0f}/month"):
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                new_start = st.number_input("Start Year", 1, key=f"start_{i}", value=start)
            with col2:
                new_end = st.number_input("End Year", 1, key=f"end_{i}", value=end)
            with col3:
                new_amt = st.number_input("Monthly Amount ($)", 0, key=f"amt_{i}", value=amt, step=500)
            with col4:
                if st.button("🗑️ Remove", key=f"remove_{i}"):
                    periods_to_remove.append(i)
            
            # Update the period if values changed
            if new_start != start or new_end != end or new_amt != amt:
                st.session_state.investment_periods[i] = (new_start, new_end, new_amt)
    
    # Remove marked periods
    for i in reversed(periods_to_remove):
        if len(st.session_state.investment_periods) > 1:  # Keep at least one period
            st.session_state.investment_periods.pop(i)
            st.rerun()
    
    # Convert years → months
    monthly_plan = [
        ((s - 1) * 12 + 1, e * 12, amt)
        for s, e, amt in st.session_state.investment_periods
        if s <= e and amt > 0
    ]

    # ---------- Run simulation ----------
    if st.button("🚀 Run Simulation", type="primary", key="main_run_simulation"):
        data = run_sim(
            monthly_plan=monthly_plan,
            roth_ira_cap=roth_cap,
            roth_ira_enabled=enable_roth,
            k401_cap=k401_cap,
            k401_enabled=enable_k401,
            simulation_months=sim_months,
            roth_ira_return=roth_r,
            k401_return=k401_r,
            dca_return=dca_r,
            stock_return=stock_r,
            dca_ratio=dca_ratio,
            stock_ratio=stock_ratio,
            inflation_rate=inflation_rate,
            initial_roth=initial_roth,
            initial_401k=initial_401k,
            initial_dca=initial_dca,
            initial_stock=initial_stock,
        )
        # ---------- Metrics ----------
        st.header("📊 Results")
        
        # Create tabs for nominal vs inflation-adjusted
        tab1, tab2 = st.tabs(["💰 Nominal Values", "📈 Inflation-Adjusted Values"])
        
        with tab1:
            col1, col2, col3, col4 = st.columns(4)
            final_total = data["Total"][-1]
            initial_total = data["Total"][0]
            growth = final_total - initial_total
            pct = (growth / initial_total) * 100 if initial_total > 0 else 0
            col1.metric("Final Portfolio Value", f"${final_total:,.0f}")
            col2.metric("Total Growth", f"${growth:,.0f}")
            col3.metric("Total Return", f"{pct:.1f}%")
            col4.metric("Years Simulated", sim_years)
        
        with tab2:
            col1, col2, col3, col4 = st.columns(4)
            final_total_adj = data["Total_Adjusted"][-1]
            initial_total_adj = data["Total_Adjusted"][0]
            growth_adj = final_total_adj - initial_total_adj
            pct_adj = (growth_adj / initial_total_adj) * 100 if initial_total_adj > 0 else 0
            col1.metric("Final Portfolio Value (Real)", f"${final_total_adj:,.0f}")
            col2.metric("Total Growth (Real)", f"${growth_adj:,.0f}")
            col3.metric("Total Return (Real)", f"{pct_adj:.1f}%")
            col4.metric("Inflation Rate", f"{inflation_rate*100:.1f}%")

        # ---------- Portfolio growth chart ----------
        st.subheader("📈 Portfolio Growth Over Time")

        # Create tabs for charts
        chart_tab1, chart_tab2 = st.tabs(["💰 Nominal Growth", "📈 Real Growth (Inflation-Adjusted)"])

        with chart_tab1:
            # Create data for nominal line chart
            chart_data = []
            for i, month in enumerate(data["Month"]):
                year = month / 12
                chart_data.extend([
                    {"Year": year, "Component": "Total", "Value": data["Total"][i]},
                    {"Year": year, "Component": "Roth IRA", "Value": data["Roth IRA"][i]},
                    {"Year": year, "Component": "401(k)", "Value": data["401(k)"][i]},
                    {"Year": year, "Component": "ETF DCA", "Value": data["ETF DCA"][i]},
                    {"Year": year, "Component": "Stock Picks", "Value": data["Stock Picks"][i]}
                ])

            # Create nominal line chart
            try:
                line_chart = (
                    alt.Chart(alt.Data(values=chart_data))
                        .mark_line(opacity=0.85, strokeWidth=3)
                        .encode(
                            x=alt.X("Year:Q", title="Years"),
                            y=alt.Y("Value:Q", title="Portfolio Value ($)", 
                                    axis=alt.Axis(format="$~s")),
                            color="Component:N",
                            tooltip=[
                                "Component:N",
                                alt.Tooltip("Year:Q", format=".1f"),
                                alt.Tooltip("Value:Q", format="$.2~s")
                            ]
                        )
                        .interactive()
                )
                
                st.altair_chart(line_chart, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error creating nominal chart: {str(e)}")
                st.info("Displaying data table instead...")
                
                # Fallback: show data table
                st.subheader("📊 Nominal Portfolio Data")
                for i, month in enumerate(data["Month"]):
                    if i % 12 == 0:  # Show yearly data
                        year = month // 12
                        st.write(f"**Year {year}:**")
                        st.write(f"  Total: ${data['Total'][i]:,.2f}")
                        st.write(f"  Roth IRA: ${data['Roth IRA'][i]:,.2f}")
                        st.write(f"  401(k): ${data['401(k)'][i]:,.2f}")
                        st.write(f"  ETF DCA: ${data['ETF DCA'][i]:,.2f}")
                        st.write(f"  Stock Picks: ${data['Stock Picks'][i]:,.2f}")
                        st.write("---")

        with chart_tab2:
            # Create data for inflation-adjusted line chart
            chart_data_adj = []
            for i, month in enumerate(data["Month"]):
                year = month / 12
                chart_data_adj.extend([
                    {"Year": year, "Component": "Total", "Value": data["Total_Adjusted"][i]},
                    {"Year": year, "Component": "Roth IRA", "Value": data["Roth IRA_Adjusted"][i]},
                    {"Year": year, "Component": "401(k)", "Value": data["401(k)_Adjusted"][i]},
                    {"Year": year, "Component": "ETF DCA", "Value": data["ETF DCA_Adjusted"][i]},
                    {"Year": year, "Component": "Stock Picks", "Value": data["Stock Picks_Adjusted"][i]}
                ])

            # Create inflation-adjusted line chart
            try:
                line_chart_adj = (
                    alt.Chart(alt.Data(values=chart_data_adj))
                        .mark_line(opacity=0.85, strokeWidth=3)
                        .encode(
                            x=alt.X("Year:Q", title="Years"),
                            y=alt.Y("Value:Q", title="Real Portfolio Value ($)", 
                                    axis=alt.Axis(format="$~s")),
                            color="Component:N",
                            tooltip=[
                                "Component:N",
                                alt.Tooltip("Year:Q", format=".1f"),
                                alt.Tooltip("Value:Q", format="$.2~s")
                            ]
                        )
                        .interactive()
                )
                
                st.altair_chart(line_chart_adj, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error creating inflation-adjusted chart: {str(e)}")
                st.info("Displaying data table instead...")
                
                # Fallback: show data table
                st.subheader("📊 Real Portfolio Data (Inflation-Adjusted)")
                for i, month in enumerate(data["Month"]):
                    if i % 12 == 0:  # Show yearly data
                        year = month // 12
                        st.write(f"**Year {year}:**")
                        st.write(f"  Total: ${data['Total_Adjusted'][i]:,.2f}")
                        st.write(f"  Roth IRA: ${data['Roth IRA_Adjusted'][i]:,.2f}")
                        st.write(f"  401(k): ${data['401(k)_Adjusted'][i]:,.2f}")
                        st.write(f"  ETF DCA: ${data['ETF DCA_Adjusted'][i]:,.2f}")
                        st.write(f"  Stock Picks: ${data['Stock Picks_Adjusted'][i]:,.2f}")
                        st.write("---")

        # ---------- Allocation breakdown ----------
        st.subheader("📋 Final Allocation")

        # Create tabs for allocation breakdown
        alloc_tab1, alloc_tab2 = st.tabs(["💰 Nominal Allocation", "📈 Real Allocation (Inflation-Adjusted)"])

        with alloc_tab1:
            final_vals = {k: data[k][-1] for k in (
                "Roth IRA", "401(k)", "ETF DCA", "Stock Picks"
            )}

            pairs = [(k, float(v)) for k, v in final_vals.items()
                     if v is not None and v > 0]

            if pairs:                                # ← at least one bucket has value
                labels, raw_sizes = zip(*pairs)

                # Convert to simple Python list
                sizes = [float(x) for x in raw_sizes]

                fig2, (pie_ax, bar_ax) = plt.subplots(1, 2, figsize=(15, 6))

                # Skip pie if only one slice (pure UX)
                if len(sizes) > 1:
                    pie_ax.pie(
                        sizes,
                        labels=labels,
                        autopct="%1.1f%%",
                        startangle=90,
                        counterclock=False,
                    )
                else:
                    pie_ax.text(0.5, 0.5, "100 %", ha="center", va="center", fontsize=24)
                
                pie_ax.set_title("Final Portfolio Allocation (Nominal)")

                bar_ax.bar(labels, sizes)
                bar_ax.set_ylabel("Value ($)")
                bar_ax.yaxis.set_major_formatter(
                    plt.FuncFormatter(lambda x, _: f"${x:,.0f}")
                )
                bar_ax.set_title("Final Portfolio Values (Nominal)")

                plt.tight_layout()
                st.pyplot(fig2, use_container_width=True)
                plt.close(fig2)  # Release resources

            else:
                st.info("No money was contributed to any bucket → nothing to plot.")

        with alloc_tab2:
            final_vals_adj = {k: data[k][-1] for k in (
                "Roth IRA_Adjusted", "401(k)_Adjusted", "ETF DCA_Adjusted", "Stock Picks_Adjusted"
            )}

            pairs_adj = [(k.replace("_Adjusted", ""), float(v)) for k, v in final_vals_adj.items()
                         if v is not None and v > 0]

            if pairs_adj:                                # ← at least one bucket has value
                labels_adj, raw_sizes_adj = zip(*pairs_adj)

                # Convert to simple Python list
                sizes_adj = [float(x) for x in raw_sizes_adj]

                fig3, (pie_ax_adj, bar_ax_adj) = plt.subplots(1, 2, figsize=(15, 6))

                # Skip pie if only one slice (pure UX)
                if len(sizes_adj) > 1:
                    pie_ax_adj.pie(
                        sizes_adj,
                        labels=labels_adj,
                        autopct="%1.1f%%",
                        startangle=90,
                        counterclock=False,
                    )
                else:
                    pie_ax_adj.text(0.5, 0.5, "100 %", ha="center", va="center", fontsize=24)
                
                pie_ax_adj.set_title("Final Portfolio Allocation (Real)")

                bar_ax_adj.bar(labels_adj, sizes_adj)
                bar_ax_adj.set_ylabel("Real Value ($)")
                bar_ax_adj.yaxis.set_major_formatter(
                    plt.FuncFormatter(lambda x, _: f"${x:,.0f}")
                )
                bar_ax_adj.set_title("Final Portfolio Values (Real)")

                plt.tight_layout()
                st.pyplot(fig3, use_container_width=True)
                plt.close(fig3)  # Release resources

            else:
                st.info("No money was contributed to any bucket → nothing to plot.")

        # ---------- Data table (yearly rows only) ----------
        st.subheader("📈 Yearly Data")
        
        # Create tabs for yearly data
        yearly_tab1, yearly_tab2 = st.tabs(["💰 Nominal Yearly Data", "📈 Real Yearly Data (Inflation-Adjusted)"])
        
        with yearly_tab1:
            # Create yearly data from lists (nominal)
            yearly_data = []
            for i, month in enumerate(data["Month"]):
                if month % 12 == 0:  # Only yearly data
                    yearly_data.append({
                        "Year": month // 12,
                        "Total": data["Total"][i],
                        "Roth IRA": data["Roth IRA"][i],
                        "401(k)": data["401(k)"][i],
                        "ETF DCA": data["ETF DCA"][i],
                        "Stock Picks": data["Stock Picks"][i]
                    })
            
            if yearly_data:
                # Display as a simple table without pandas
                st.write("**Yearly Portfolio Values (Nominal):**")
                for row in yearly_data:
                    st.write(f"**Year {row['Year']}:**")
                    st.write(f"  Total: ${row['Total']:,.2f}")
                    st.write(f"  Roth IRA: ${row['Roth IRA']:,.2f}")
                    st.write(f"  401(k): ${row['401(k)']:,.2f}")
                    st.write(f"  ETF DCA: ${row['ETF DCA']:,.2f}")
                    st.write(f"  Stock Picks: ${row['Stock Picks']:,.2f}")
                    st.write("---")
            else:
                st.info("No yearly data to display.")

        with yearly_tab2:
            # Create yearly data from lists (inflation-adjusted)
            yearly_data_adj = []
            for i, month in enumerate(data["Month"]):
                if month % 12 == 0:  # Only yearly data
                    yearly_data_adj.append({
                        "Year": month // 12,
                        "Total": data["Total_Adjusted"][i],
                        "Roth IRA": data["Roth IRA_Adjusted"][i],
                        "401(k)": data["401(k)_Adjusted"][i],
                        "ETF DCA": data["ETF DCA_Adjusted"][i],
                        "Stock Picks": data["Stock Picks_Adjusted"][i]
                    })
            
            if yearly_data_adj:
                # Display as a simple table without pandas
                st.write("**Yearly Portfolio Values (Real - Inflation-Adjusted):**")
                for row in yearly_data_adj:
                    st.write(f"**Year {row['Year']}:**")
                    st.write(f"  Total: ${row['Total']:,.2f}")
                    st.write(f"  Roth IRA: ${row['Roth IRA']:,.2f}")
                    st.write(f"  401(k): ${row['401(k)']:,.2f}")
                    st.write(f"  ETF DCA: ${row['ETF DCA']:,.2f}")
                    st.write(f"  Stock Picks: ${row['Stock Picks']:,.2f}")
                    st.write("---")
            else:
                st.info("No yearly data to display.")

# -----------------------------------------------------------
# 🚀  Entry point
# -----------------------------------------------------------
if __name__ == "__main__":
    main()
