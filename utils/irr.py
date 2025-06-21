import numpy_financial as npf

def calculate_irr(cash_flows):
    """
    Calculate IRR assuming equal time intervals between cash flows.
    Uses numpy_financial.irr which returns a monthly IRR.
    Converts to annualized IRR.
    """
    if len(cash_flows) < 2 or all(cf == 0 for cf in cash_flows):
        return 0.0
    
    monthly_irr = npf.irr(cash_flows)

    if monthly_irr is None or monthly_irr <= -1:
        return 0.0
    
    annual_irr = (1 + monthly_irr) ** 12 - 1
    return annual_irr
