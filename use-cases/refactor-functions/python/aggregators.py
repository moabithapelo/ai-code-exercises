"""
Data grouping and aggregation logic.
"""

from typing import Dict, List, Optional


def group_sales_data(sales_data: List[Dict], grouping: str) -> Dict:
    """
    Group sales data by specified field and calculate aggregates.
    
    Args:
        sales_data: List of sales transactions
        grouping: Field name to group by
    
    Returns:
        Dictionary with grouped data
    """
    grouped = {}
    
    for sale in sales_data:
        key = sale.get(grouping, 'Unknown')
        if key not in grouped:
            grouped[key] = {
                'count': 0,
                'total': 0,
                'items': []
            }
        
        grouped[key]['count'] += 1
        grouped[key]['total'] += sale['amount']
        grouped[key]['items'].append(sale)
    
    # Calculate averages
    for key in grouped:
        grouped[key]['average'] = grouped[key]['total'] / grouped[key]['count']
    
    return grouped