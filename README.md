# 💰 Interactive Investment Calculator

A modular Streamlit application for simulating compound investment growth across multiple account types with inflation adjustment.

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run main.py
```

## 📊 Features

- **Multi-Account Simulation**: Roth IRA, 401(k), ETF DCA, Stock Picks
- **Flexible Investment Periods**: Define different contribution amounts over time
- **Inflation Adjustment**: Real vs nominal value calculations
- **Advanced Metrics**: IRR, CAGR, Total Return based on total invested
- **Interactive Charts**: Portfolio growth visualization with Altair
- **Allocation Breakdown**: Pie charts and bar charts for final portfolio

## 🏗️ Project Structure

```
investment/
├── main.py                    # Main application entry point
├── models/
│   └── simulation.py         # Core simulation logic
├── utils/
│   └── irr.py               # IRR calculation utilities
├── components/
│   ├── sidebar.py           # Sidebar controls
│   ├── periods.py           # Investment periods editor
│   ├── results.py           # Results display (4-column layout)
│   ├── charts.py            # Portfolio growth charts
│   ├── allocation.py        # Final allocation breakdown
│   └── yearly_data.py       # Yearly data tables
└── requirements.txt
```

## 📈 Key Metrics

- **Total Return**: Based on total invested (initial + contributions)
- **IRR (内部收益率)**: Internal Rate of Return
- **CAGR (年化收益率)**: Compound Annual Growth Rate
- **Inflation-Adjusted Values**: Real purchasing power over time

## 🎛️ Usage

1. Set initial account balances in sidebar
2. Configure return rates for each investment type
3. Define investment periods and monthly contributions
4. Click "Run Simulation" to see results
5. View charts, allocation breakdown, and yearly data

## 🔧 Dependencies

- `streamlit`: Web application framework
- `matplotlib`: Charts and visualizations
- `altair`: Interactive data visualization 