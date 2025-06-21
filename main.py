import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from models.simulation import compound_growth_with_visualization
from utils.irr import calculate_irr
from components.sidebar import sidebar_controls
from components.periods import periods_editor
from components.results import display_results
from components.charts import display_portfolio_charts
from components.allocation import display_allocation_breakdown
from components.yearly_data import display_yearly_data

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
# 🎛  Interactive UI
# -----------------------------------------------------------
def main():
    st.title("💰 Interactive Investment Calculator")
    st.markdown("---")

    # ---------- Sidebar controls ----------
    with st.sidebar:
        sidebar_params = sidebar_controls()

    # ---------- Period configuration ----------
    monthly_plan = periods_editor()

    # ---------- Run simulation ----------
    if st.button("🚀 Run Simulation", type="primary", key="main_run_simulation"):
        data = compound_growth_with_visualization(
            monthly_plan=monthly_plan,
            roth_ira_cap=sidebar_params["roth_cap"],
            roth_ira_enabled=sidebar_params["enable_roth"],
            k401_cap=sidebar_params["k401_cap"],
            k401_enabled=sidebar_params["enable_k401"],
            simulation_months=sidebar_params["sim_months"],
            roth_ira_return=sidebar_params["roth_r"],
            k401_return=sidebar_params["k401_r"],
            dca_return=sidebar_params["dca_r"],
            stock_return=sidebar_params["stock_r"],
            dca_ratio=sidebar_params["dca_ratio"],
            stock_ratio=sidebar_params["stock_ratio"],
            inflation_rate=sidebar_params["inflation_rate"],
            initial_roth=sidebar_params["initial_roth"],
            initial_401k=sidebar_params["initial_401k"],
            initial_dca=sidebar_params["initial_dca"],
            initial_stock=sidebar_params["initial_stock"],
        )
        
        # ---------- Display Results ----------
        display_results(
            data=data,
            sim_years=sidebar_params["sim_years"],
            sim_months=sidebar_params["sim_months"],
            inflation_rate=sidebar_params["inflation_rate"]
        )

        # ---------- Portfolio growth chart ----------
        display_portfolio_charts(data)

        # ---------- Allocation breakdown ----------
        display_allocation_breakdown(data)

        # ---------- Data table (yearly rows only) ----------
        display_yearly_data(data)

if __name__ == "__main__":
    main() 