"""
Output formatting functions.
Convert report data to final format.
"""

from typing import Dict


def generate_empty_report(report_type: str, output_format: str):
    """
    Generate an empty report when no data matches criteria.
    
    Args:
        report_type: Type of report
        output_format: Output format
    
    Returns:
        Empty report in requested format
    """
    if output_format == 'json':
        return {"message": "No data matches the specified criteria", "data": []}
    
    # For other formats, create minimal report file
    filename = f"empty_{report_type}_report.{output_format}"
    with open(filename, 'w') as f:
        f.write(f"Empty {report_type} report - No data matches criteria")
    
    return filename


def generate_html_report(report_data: Dict, include_charts: bool) -> str:
    """
    Generate HTML report.
    
    Args:
        report_data: Complete report data
        include_charts: Whether to include charts
    
    Returns:
        Path to generated HTML file
    """
    filename = f"sales_report_{report_data['date_generated'].replace(' ', '_').replace(':', '-')}.html"
    
    # Simple HTML generation (simplified for example)
    html_content = f"""
    <html>
        <head><title>Sales Report</title></head>
        <body>
            <h1>Sales Report</h1>
            <p>Type: {report_data['report_type']}</p>
            <p>Generated: {report_data['date_generated']}</p>
            <h2>Summary</h2>
            <p>Total Sales: {report_data['summary']['total_sales']}</p>
            <p>Transactions: {report_data['summary']['transaction_count']}</p>
        </body>
    </html>
    """
    
    with open(filename, 'w') as f:
        f.write(html_content)
    
    return filename


def generate_excel_report(report_data: Dict, include_charts: bool) -> str:
    """
    Generate Excel report (placeholder).
    
    Args:
        report_data: Complete report data
        include_charts: Whether to include charts
    
    Returns:
        Path to generated Excel file
    """
    filename = f"sales_report_{report_data['date_generated'].replace(' ', '_').replace(':', '-')}.xlsx"
    # In a real implementation, use openpyxl or pandas to create Excel
    with open(filename, 'w') as f:
        f.write("Excel report would be generated here")
    return filename


def generate_pdf_report(report_data: Dict, include_charts: bool) -> str:
    """
    Generate PDF report (placeholder).
    
    Args:
        report_data: Complete report data
        include_charts: Whether to include charts
    
    Returns:
        Path to generated PDF file
    """
    filename = f"sales_report_{report_data['date_generated'].replace(' ', '_').replace(':', '-')}.pdf"
    with open(filename, 'w') as f:
        f.write("PDF report would be generated here")
    return filename


def format_report(report_data: Dict, output_format: str, include_charts: bool):
    """
    Format report in requested output format.
    
    Args:
        report_data: Complete report data
        output_format: 'json', 'html', 'excel', or 'pdf'
        include_charts: Whether to include charts
    
    Returns:
        Formatted report
    """
    if output_format == 'json':
        return report_data
    elif output_format == 'html':
        return generate_html_report(report_data, include_charts)
    elif output_format == 'excel':
        return generate_excel_report(report_data, include_charts)
    elif output_format == 'pdf':
        return generate_pdf_report(report_data, include_charts)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")