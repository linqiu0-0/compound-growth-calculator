import streamlit as st
import altair as alt

def display_portfolio_charts(data):
    """
    Display portfolio growth charts using Altair
    """
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