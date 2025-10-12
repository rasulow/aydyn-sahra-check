from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Main page view with three sections"""
    return render(request, 'main/home.html')

def sargyt_check(request):
    """Sargyt we check page with data checking form"""
    from .models import Client, Color
    import json
    
    # Get all clients with their regions
    clients = Client.objects.select_related('region').all()
    clients_data = [
        {
            'id': client.id,
            'name': client.name,
            'region': client.region.name
        }
        for client in clients
    ]
    
    # Get all colors
    colors = Color.objects.all()
    colors_data = [
        {
            'id': color.id,
            'code': color.kod,
            'price': float(color.price)
        }
        for color in colors
    ]
    
    context = {
        'clients_json': json.dumps(clients_data),
        'colors_json': json.dumps(colors_data),
    }
    
    return render(request, 'main/sargyt_check.html', context)


@csrf_exempt
@require_POST
def download_orders_pdf(request):
    """Generate and download PDF of all orders"""
    try:
        # Import ReportLab inside function to avoid import errors if not installed
        try:
            from io import BytesIO
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch, mm
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        except ImportError as e:
            logger.error(f"ReportLab not installed: {e}")
            return JsonResponse({
                'error': 'ReportLab library is not installed. Please run: pip install reportlab'
            }, status=500)
        
        # Parse the incoming JSON data
        data = json.loads(request.body)
        orders = data.get('orders', [])
        client_name = data.get('client_name', 'Unknown')
        client_region = data.get('client_region', 'Unknown')
        
        logger.info(f"Generating PDF for client: {client_name}, orders count: {len(orders)}")
        
        # Create the PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                              rightMargin=20*mm, leftMargin=20*mm,
                              topMargin=20*mm, bottomMargin=20*mm)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=10
        )
        
        normal_style = styles['Normal']
        
        # Add title
        title = Paragraph("Sargyt we check - Order Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Add client information
        client_info = Paragraph(f"<b>Client:</b> {client_name} | <b>Region:</b> {client_region}", normal_style)
        elements.append(client_info)
        
        date_info = Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}", normal_style)
        elements.append(date_info)
        elements.append(Spacer(1, 20))
        
        # Process each order
        for idx, order in enumerate(orders, 1):
            # Order header
            order_title = Paragraph(f"Order #{idx}", heading_style)
            elements.append(order_title)
            elements.append(Spacer(1, 8))
            
            # Prepare order data table
            order_data = []
            order_data.append(['Field', 'Value'])
            
            if order.get('category'):
                order_data.append(['Category', order['category']])
            
            if order.get('karniz_gornus'):
                order_data.append(['Karniz gornus', order['karniz_gornus']])
            
            if order.get('selpe'):
                order_data.append(['Selpe', order['selpe']])
            
            if order.get('region_radio'):
                order_data.append(['Region', order['region_radio']])
            
            if order.get('weranda'):
                order_data.append(['Weranda', order['weranda']])
                if order.get('weranda_measurements'):
                    for meas in order['weranda_measurements']:
                        order_data.append([f"  {meas['label']}", f"W: {meas['width']} x H: {meas['height']}"])
            
            if order.get('measurements'):
                meas = order['measurements']
                if meas.get('top_length'):
                    order_data.append(['Top Length', str(meas['top_length'])])
                if meas.get('left_length'):
                    order_data.append(['Left Length', str(meas['left_length'])])
            
            if order.get('kod_renk'):
                colors_list = ', '.join(order['kod_renk'])
                order_data.append(['Kod renk', colors_list])
            
            # Create table
            if len(order_data) > 1:  # More than just header
                table = Table(order_data, colWidths=[2.5*inch, 4*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ]))
                elements.append(table)
            
            # Add space between orders
            elements.append(Spacer(1, 20))
            
            # Page break after every 2 orders (except the last one)
            if idx % 2 == 0 and idx < len(orders):
                elements.append(PageBreak())
        
        # Build PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer and write it to the response
        pdf = buffer.getvalue()
        buffer.close()
        
        # Create the HttpResponse with PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="sargyt_orders_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        response.write(pdf)
        
        return response
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f"Error generating PDF: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
