"""
Build the report data structure incrementally.
"""

from datetime import datetime
from typing import Dict, List, Optional


def build_base_report(
    report_type: str,
    date_range: Optional[Dict],
    filters: Optional[Dict],
    metrics: Dict,
    sales_data: List[Dict]
) -> Dict:
    """
    Create foundation report with summary information.
    
    Args:
        report_type: Type of report
        date_range: Original date range filter
        filters: Original filters
        metrics: Calculated metrics
        sales_data: Sales data (for reference)
    
    Returns:
        Base report dictionary
    """
    max_sale = metrics['max_sale']
    min_sale = metrics['min_sale']
    
    return {
        'report_type': report_type,
        'date_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_range': date_range,
        'filters': filters,
        'summary': {
            'total_sales': metrics['total_sales'],
            'transaction_count': metrics['transaction_count'],
            'average_sale': metrics['average_sale'],
            'max_sale': {
                'amount': max_sale['amount'] if max_sale else None,
                'date': max_sale['date'] if max_sale else None,
                'details': max_sale
            } if max_sale else None,
            'min_sale': {
                'amount': min_sale['amount'] if min_sale else None,
                'date': min_sale['date'] if min_sale else None,
                'details': min_sale
            } if min_sale else None
        }
    }


def add_grouping_to_report(
    report: Dict,
    grouping: str,
    grouped_data: Dict,
    total_sales: float
) -> Dict:
    """
    Enrich report with grouping data.
    
    Args:
        report: Existing report dictionary
        grouping: Field used for grouping
        grouped_data: Grouped data from aggregator
        total_sales: Total sales for percentage calculations
    
    Returns:
        Updated report dictionary
    """
    report['grouping'] = {
        'by': grouping,
        'groups': {}
    }
    
    for key, data in grouped_data.items():
        report['grouping']['groups'][key] = {
            'count': data['count'],
            'total': data['total'],
            'average': data['average'],
            'percentage': (data['total'] / total_sales) * 100 if total_sales else 0
        }
    
    return report


def add_transactions_to_report(report: Dict, sales_data: List[Dict]) -> Dict:
    """
    Add detailed transaction data.
    
    Args:
        report: Existing report dictionary
        sales_data: Sales data
    
    Returns:
        Updated report dictionary
    """
    report['transactions'] = []
    
    for sale in sales_data:
        transaction = {k: v for k, v in sale.items()}
        
        # Add calculated fields
        if 'tax' in sale and 'amount' in sale:
            transaction['pre_tax'] = sale['amount'] - sale['tax']
        
        if 'cost' in sale and 'amount' in sale:
            transaction['profit'] = sale['amount'] - sale['cost']
            if sale['amount'] > 0:
                transaction['margin'] = (transaction['profit'] / sale['amount']) * 100
        
        report['transactions'].append(transaction)
    
    return report


def handle_empty_data(report_type: str, output_format: str):
    """
    Generate appropriate empty report.
    
    Args:
        report_type: Type of report
        output_format: Output format
    
    Returns:
        Empty report in requested format
    """
    from .formatters import generate_empty_report
    return generate_empty_report(report_type, output_format)