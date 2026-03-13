"""
Main report generator function that orchestrates all helpers.
"""

from typing import Dict, List, Optional, Union

from .validators import validate_inputs, validate_grouping
from .processors import apply_all_filters
from .calculators import calculate_basic_metrics, calculate_forecast
from .aggregators import group_sales_data
from .chart_builders import generate_all_charts
from .report_builders import (
    build_base_report,
    add_grouping_to_report,
    add_transactions_to_report,
    handle_empty_data
)
from .formatters import format_report


def generate_sales_report(
    sales_data: List[Dict],
    report_type: str = 'summary',
    date_range: Optional[Dict[str, str]] = None,
    filters: Optional[Dict[str, Union[str, List]]] = None,
    grouping: Optional[str] = None,
    include_charts: bool = False,
    output_format: str = 'pdf'
):
    """
    Generate a comprehensive sales report based on provided data and parameters.
    
    Parameters:
    - sales_data: List of sales transactions with 'date' and 'amount' fields
    - report_type: 'summary', 'detailed', or 'forecast'
    - date_range: Dict with 'start' and 'end' dates (YYYY-MM-DD)
    - filters: Dict of filters to apply (key-value pairs)
    - grouping: How to group data ('product', 'category', 'customer', 'region')
    - include_charts: Whether to include charts/visualizations
    - output_format: 'pdf', 'excel', 'html', or 'json'

    Returns:
    - Report data or file path depending on output_format
    """
    # === STEP 1: Validate inputs ===
    validate_inputs(sales_data, report_type, output_format)
    validate_grouping(grouping)
    
    # === STEP 2: Create working copy ===
    working_data = sales_data.copy() if sales_data else []
    
    # === STEP 3: Apply filters ===
    working_data = apply_all_filters(working_data, date_range, filters)
    
    # === STEP 4: Handle empty data ===
    if not working_data:
        return handle_empty_data(report_type, output_format)
    
    # === STEP 5: Calculate metrics ===
    metrics = calculate_basic_metrics(working_data)
    
    # === STEP 6: Build base report ===
    report = build_base_report(
        report_type, date_range, filters, metrics, working_data
    )
    
    # === STEP 7: Add grouping if specified ===
    grouped_data = None
    if grouping:
        grouped_data = group_sales_data(working_data, grouping)
        report = add_grouping_to_report(report, grouping, grouped_data, metrics['total_sales'])
    
    # === STEP 8: Add detailed transactions if needed ===
    if report_type == 'detailed':
        report = add_transactions_to_report(report, working_data)
    
    # === STEP 9: Add forecast if needed ===
    if report_type == 'forecast':
        report['forecast'] = calculate_forecast(working_data)
    
    # === STEP 10: Add charts if requested ===
    if include_charts:
        report['charts'] = generate_all_charts(working_data, grouping, grouped_data)
    
    # === STEP 11: Format and return ===
    return format_report(report, output_format, include_charts)