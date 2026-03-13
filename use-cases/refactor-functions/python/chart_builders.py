"""
Prepare data structures for charts and visualizations.
"""

from typing import Dict, List, Optional


def generate_time_series_chart(sales_data: List[Dict]) -> Dict:
    """
    Generate time series chart data (sales over time).
    
    Args:
        sales_data: List of sales transactions
    
    Returns:
        Dictionary with chart data
    """
    date_sales = {}
    
    for sale in sales_data:
        if sale['date'] not in date_sales:
            date_sales[sale['date']] = 0
        date_sales[sale['date']] += sale['amount']
    
    chart = {
        'labels': [],
        'data': []
    }
    
    for date in sorted(date_sales.keys()):
        chart['labels'].append(date)
        chart['data'].append(date_sales[date])
    
    return chart


def generate_pie_chart(grouped_data: Dict, grouping: str) -> Dict:
    """
    Generate pie chart data for grouped sales.
    
    Args:
        grouped_data: Grouped sales data from aggregator
        grouping: Field name used for grouping
    
    Returns:
        Dictionary with chart data
    """
    chart = {
        'labels': [],
        'data': []
    }
    
    for key, data in grouped_data.items():
        chart['labels'].append(key)
        chart['data'].append(data['total'])
    
    return chart


def generate_all_charts(
    sales_data: List[Dict],
    grouping: Optional[str] = None,
    grouped_data: Optional[Dict] = None
) -> Dict:
    """
    Generate all requested charts.
    
    Args:
        sales_data: List of sales transactions
        grouping: Optional grouping field
        grouped_data: Optional pre-grouped data
    
    Returns:
        Dictionary with all charts
    """
    charts = {
        'sales_over_time': generate_time_series_chart(sales_data)
    }
    
    if grouping and grouped_data:
        charts[f'sales_by_{grouping}'] = generate_pie_chart(grouped_data, grouping)
    
    return charts