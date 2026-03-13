# validators.py
"""
Input validation functions for the sales report generator.
All functions focus ONLY on validation and raising appropriate errors.
No data transformation or business logic.
"""

from datetime import datetime
from typing import Any, Dict, List, Union



def validate_inputs(sales_data: List[Dict], report_type: str, output_format: str) -> None:
    """
    Validate core input parameters.
    
    Args:
        sales_data: List of sales transactions
        report_type: 'summary', 'detailed', or 'forecast'
        output_format: 'pdf', 'excel', 'html', or 'json'
    
    Raises:
        ValueError: If any parameter is invalid
    """
    # Validate sales_data
    if sales_data is None:
        raise ValueError("Sales data cannot be None")
    
    if not isinstance(sales_data, list):
        raise ValueError(f"Sales data must be a list, got {type(sales_data).__name__}")
    
    # Empty list is valid (will be handled later), but must be list
    if not sales_data:
        return  # Empty list is acceptable
    
    # Validate each sale has required fields (optional - depends on requirements)
    required_fields = ['date', 'amount']
    for i, sale in enumerate(sales_data):
        if not isinstance(sale, dict):
            raise ValueError(f"Sale at index {i} must be a dictionary, got {type(sale).__name__}")
        
        for field in required_fields:
            if field not in sale:
                raise ValueError(f"Sale at index {i} missing required field: '{field}'")
    
    # Validate report_type
    valid_report_types = ['summary', 'detailed', 'forecast']
    if report_type not in valid_report_types:
        raise ValueError(
            f"Invalid report_type: '{report_type}'. "
            f"Must be one of: {', '.join(valid_report_types)}"
        )
    
    # Validate output_format
    valid_output_formats = ['pdf', 'excel', 'html', 'json']
    if output_format not in valid_output_formats:
        raise ValueError(
            f"Invalid output_format: '{output_format}'. "
            f"Must be one of: {', '.join(valid_output_formats)}"
        )


def validate_date_range(date_range: Dict[str, str]) -> tuple:
    """
    Validate and parse date range dictionary.
    
    Args:
        date_range: Dictionary with 'start' and 'end' date strings (YYYY-MM-DD)
    
    Returns:
        tuple: (start_date, end_date) as datetime objects
    
    Raises:
        ValueError: If date_range is invalid
    """
    # Validate structure
    if date_range is None:
        raise ValueError("date_range cannot be None")
    
    if not isinstance(date_range, dict):
        raise ValueError(f"date_range must be a dictionary, got {type(date_range).__name__}")
    
    # Validate required keys
    if 'start' not in date_range:
        raise ValueError("date_range must contain 'start' key")
    
    if 'end' not in date_range:
        raise ValueError("date_range must contain 'end' key")
    
    # Validate types
    if not isinstance(date_range['start'], str):
        raise ValueError(f"date_range['start'] must be string, got {type(date_range['start']).__name__}")
    
    if not isinstance(date_range['end'], str):
        raise ValueError(f"date_range['end'] must be string, got {type(date_range['end']).__name__}")
    
    # Parse and validate dates
    try:
        start_date = datetime.strptime(date_range['start'], '%Y-%m-%d')
    except ValueError as e:
        raise ValueError(f"Invalid start date format: '{date_range['start']}'. Expected YYYY-MM-DD") from e
    
    try:
        end_date = datetime.strptime(date_range['end'], '%Y-%m-%d')
    except ValueError as e:
        raise ValueError(f"Invalid end date format: '{date_range['end']}'. Expected YYYY-MM-DD") from e
    
    # Validate logical relationship
    if start_date > end_date:
        raise ValueError(f"Start date ({date_range['start']}) cannot be after end date ({date_range['end']})")
    
    return start_date, end_date


def validate_filters(filters: Dict[str, Union[str, List]]) -> None:
    """
    Validate filter structure (not apply them).
    
    Args:
        filters: Dictionary of filters to apply
    
    Raises:
        ValueError: If filters structure is invalid
    """
    if filters is None:
        raise ValueError("filters cannot be None")
    
    if not isinstance(filters, dict):
        raise ValueError(f"filters must be a dictionary, got {type(filters).__name__}")
    
    # Optional: Validate filter values if you have a known filter schema
    # For example, if you only allow filtering on certain fields:
    allowed_filter_fields = ['product', 'category', 'customer', 'region', 'payment_method']
    
    for key, value in filters.items():
        if key not in allowed_filter_fields:
            # This could be a warning instead of error, depending on requirements
            import warnings
            warnings.warn(f"Filter field '{key}' is not in standard filter list: {allowed_filter_fields}")
        
        # Validate value types
        if value is None:
            raise ValueError(f"Filter value for '{key}' cannot be None")
        
        if not isinstance(value, (str, int, float, list)):
            raise ValueError(
                f"Filter value for '{key}' must be string, number, or list, "
                f"got {type(value).__name__}"
            )
        
        # If it's a list, check contents
        if isinstance(value, list):
            if not value:
                raise ValueError(f"Filter list for '{key}' cannot be empty")
            
            for item in value:
                if not isinstance(item, (str, int, float)):
                    raise ValueError(
                        f"Filter list item for '{key}' must be string or number, "
                        f"got {type(item).__name__}"
                    )


def validate_grouping(grouping: str) -> None:
    """
    Validate grouping parameter.
    
    Args:
        grouping: Field name to group by
    
    Raises:
        ValueError: If grouping is invalid
    """
    if grouping is None:
        return  # None is valid (no grouping)
    
    if not isinstance(grouping, str):
        raise ValueError(f"grouping must be a string, got {type(grouping).__name__}")
    
    # Optional: Validate against allowed grouping fields
    allowed_grouping_fields = ['product', 'category', 'customer', 'region']
    
    if grouping not in allowed_grouping_fields:
        import warnings
        warnings.warn(
            f"Grouping field '{grouping}' may not produce expected results. "
            f"Standard grouping fields: {allowed_grouping_fields}"
        )


def validate_report_parameters(
    sales_data: List[Dict],
    report_type: str,
    date_range: Dict[str, str] = None,
    filters: Dict[str, Union[str, List]] = None,
    grouping: str = None,
    output_format: str = 'pdf'
) -> None:
    """
    Comprehensive validation of all report parameters.
    
    This is a convenience function that calls all other validators.
    
    Args:
        sales_data: List of sales transactions
        report_type: 'summary', 'detailed', or 'forecast'
        date_range: Dict with 'start' and 'end' dates (optional)
        filters: Dict of filters to apply (optional)
        grouping: Field to group by (optional)
        output_format: 'pdf', 'excel', 'html', or 'json'
    
    Raises:
        ValueError: If any parameter is invalid
    """
    validate_inputs(sales_data, report_type, output_format)
    
    if date_range is not None:
        validate_date_range(date_range)
    
    if filters is not None:
        validate_filters(filters)
    
    if grouping is not None:
        validate_grouping(grouping)
# processors.py (or data_filters.py)
"""
Data filtering and transformation functions.
These functions APPLY filters, not validate them.
"""




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
        except (KeyError, ValueError) as e:
            # Log the error and skip this sale
            import logging
            logging.warning(f"Skipping sale due to date error: {e}")
            continue
    
    return filtered


def apply_filters(sales_data: List[Dict], filters: Dict[str, Union[str, List]]) -> List[Dict]:
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
    date_range: Dict[str, str] = None,
    filters: Dict[str, Union[str, List]] = None
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
    working_data = sales_data.copy()
    
    # Apply date filter first (if provided)
    if date_range:
        from .validators import validate_date_range  # Import here to avoid circular imports
        start_date, end_date = validate_date_range(date_range)
        working_data = filter_by_date_range(working_data, start_date, end_date)
    
    # Apply other filters next
    if filters:
        from .validators import validate_filters
        validate_filters(filters)
        working_data = apply_filters(working_data, filters)
    
    return working_data