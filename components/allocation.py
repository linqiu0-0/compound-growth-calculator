import streamlit as st
import matplotlib.pyplot as plt

def display_allocation_breakdown(data):
    """
    Display final allocation breakdown with pie charts and bar charts
    """
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