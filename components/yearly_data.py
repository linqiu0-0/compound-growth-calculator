import streamlit as st

def display_yearly_data(data):
    """
    Display yearly portfolio data in table format
    """
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