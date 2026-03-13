"""
Mathematical calculations and trend analysis.
Pure functions with no side effects.
"""

from datetime import datetime
from typing import Dict, List, Optional


def calculate_basic_metrics(sales_data: List[Dict]) -> Dict:
    """
    Calculate total, average, max, and min sales.
    
    Args:
        sales_data: List of sales transactions
    
    Returns:
        Dictionary with metrics
    """
    if not sales_data:
        return {
            'total_sales': 0,
            'transaction_count': 0,
            'average_sale': 0,
            'max_sale': None,
            'min_sale': None
        }
    
    total_sales = sum(sale['amount'] for sale in sales_data)
    avg_sale = total_sales / len(sales_data)
    
    max_sale = max(sales_data, key=lambda x: x['amount'])
    min_sale = min(sales_data, key=lambda x: x['amount'])
    
    return {
        'total_sales': total_sales,
        'transaction_count': len(sales_data),
        'average_sale': avg_sale,
        'max_sale': max_sale,
        'min_sale': min_sale
    }


def calculate_forecast(sales_data: List[Dict]) -> Dict:
    """
    Calculate monthly trends and generate 3-month forecast.
    
    Args:
        sales_data: List of sales transactions
    
    Returns:
        Dictionary with forecast data
    """
    if len(sales_data) < 2:
        return {
            'monthly_sales': {},
            'growth_rates': {},
            'average_growth_rate': 0,
            'projected_sales': {}
        }
    
    # Group sales by month
    monthly_sales = {}
    for sale in sales_data:
        sale_date = datetime.strptime(sale['date'], '%Y-%m-%d')
        month_key = f"{sale_date.year}-{sale_date.month:02d}"
        monthly_sales[month_key] = monthly_sales.get(month_key, 0) + sale['amount']
    
    # Sort months and calculate growth rates
    sorted_months = sorted(monthly_sales.keys())
    growth_rates = []
    
    for i in range(1, len(sorted_months)):
        prev = monthly_sales[sorted_months[i-1]]
        curr = monthly_sales[sorted_months[i]]
        if prev > 0:
            growth_rates.append(((curr - prev) / prev) * 100)
    
    avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0
    
    # Generate 3-month forecast
    forecast = {}
    if sorted_months:
        last_month = sorted_months[-1]
        last_amount = monthly_sales[last_month]
        year, month = map(int, last_month.split('-'))
        
        for i in range(1, 4):
            month += 1
            if month > 12:
                month = 1
                year += 1
            forecast_month = f"{year}-{month:02d}"
            forecast_amount = last_amount * (1 + (avg_growth_rate / 100))
            forecast[forecast_month] = forecast_amount
            last_amount = forecast_amount
    
    return {
        'monthly_sales': monthly_sales,
        'growth_rates': {sorted_months[i]: growth_rates[i-1] 
                        for i in range(1, len(sorted_months))},
        'average_growth_rate': avg_growth_rate,
        'projected_sales': forecast
    }