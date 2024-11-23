from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

def generate_analytics_pdf(project, analytics_data):
    """Generate a PDF report for project analytics"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph(f"Analytics Report: {project.title}", title_style))
    story.append(Spacer(1, 12))

    # Overview Section
    story.append(Paragraph("Overview", styles['Heading2']))
    overview_data = [
        ["Total Views", str(analytics_data.get('view_count', 0))],
        ["Unique Visitors", str(analytics_data.get('unique_visitors', 0))],
        ["GitHub Clicks", str(analytics_data.get('github_clicks', 0))],
    ]
    overview_table = Table(overview_data, colWidths=[2*inch, 2*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 20))

    # Traffic Sources
    story.append(Paragraph("Traffic Sources", styles['Heading2']))
    traffic_data = [
        ["Direct", f"{analytics_data.get('direct_traffic', 0)}%"],
        ["Social", f"{analytics_data.get('social_traffic', 0)}%"],
        ["Search", f"{analytics_data.get('search_traffic', 0)}%"],
        ["Referral", f"{analytics_data.get('referral_traffic', 0)}%"],
    ]
    traffic_table = Table(traffic_data, colWidths=[2*inch, 2*inch])
    traffic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(traffic_table)
    story.append(Spacer(1, 20))

    # Device Distribution
    story.append(Paragraph("Device Distribution", styles['Heading2']))
    device_data = [
        ["Desktop", f"{analytics_data.get('desktop_visits', 0)}%"],
        ["Mobile", f"{analytics_data.get('mobile_visits', 0)}%"],
        ["Tablet", f"{analytics_data.get('tablet_visits', 0)}%"],
    ]
    device_table = Table(device_data, colWidths=[2*inch, 2*inch])
    device_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(device_table)

    # Build PDF
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf