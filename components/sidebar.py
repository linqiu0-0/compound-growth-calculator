import streamlit as st

def sidebar_controls():
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

    return dict(
        initial_roth=initial_roth,
        initial_401k=initial_401k,
        initial_dca=initial_dca,
        initial_stock=initial_stock,
        sim_years=sim_years,
        sim_months=sim_months,
        roth_r=roth_r,
        k401_r=k401_r,
        dca_r=dca_r,
        stock_r=stock_r,
        enable_roth=enable_roth,
        roth_cap=roth_cap,
        enable_k401=enable_k401,
        k401_cap=k401_cap,
        dca_ratio=dca_ratio,
        stock_ratio=stock_ratio,
        inflation_rate=inflation_rate,
    ) 