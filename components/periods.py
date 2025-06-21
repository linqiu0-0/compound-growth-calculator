import streamlit as st

def periods_editor():
    """
    Handle investment period editing and return the monthly plan
    """
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
    
    return monthly_plan 