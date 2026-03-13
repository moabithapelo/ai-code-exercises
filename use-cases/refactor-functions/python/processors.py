"""
Data filtering and transformation functions.
These functions APPLY filters, not validate them.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union


def filter_by_date_range(sales_data: List[Dict], start_date: datetime, end_date: datetime) -> List[Dict]:
    """
    Filter sales data to include only transactions within date range.
    
    Args:
        sales_data: List of sales transactions
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
    
    Returns:
        Filtered list of sales transactions
    """
    filtered = []
    for sale in sales_data:
        try:
            sale_date = datetime.strptime(sale['date'], '%Y-%m-%d')
            if start_date <= sale_date <= end_date:
                filtered.append(sale)
        except (KeyError, ValueError):
            # Skip invalid sales (they should have been validated)
            continue
    
    return filtered


def apply_key_value_filters(sales_data: List[Dict], filters: Dict[str, Union[str, List]]) -> List[Dict]:
    """
    Apply key-value filters to sales data.
    
    Args:
        sales_data: List of sales transactions
        filters: Dictionary of filters to apply
    
    Returns:
        Filtered list of sales transactions
    """
    filtered = sales_data.copy()
    
    for key, value in filters.items():
        if isinstance(value, list):
            filtered = [sale for sale in filtered if sale.get(key) in value]
        else:
            filtered = [sale for sale in filtered if sale.get(key) == value]
    
    return filtered


def apply_all_filters(
    sales_data: List[Dict],
    date_range: Optional[Dict[str, str]] = None,
    filters: Optional[Dict[str, Union[str, List]]] = None
) -> List[Dict]:
    """
    Apply all filters in the correct order.
    
    Args:
        sales_data: Original sales data
        date_range: Optional date range filter
        filters: Optional key-value filters
    
    Returns:
        Filtered sales data
    """
    from .validators import validate_date_range, validate_filters
    
    working_data = sales_data.copy()
    
    if date_range:
        start_date, end_date = validate_date_range(date_range)
        working_data = filter_by_date_range(working_data, start_date, end_date)
    
    if filters:
        validate_filters(filters)
        working_data = apply_key_value_filters(working_data, filters)
    
    return working_data