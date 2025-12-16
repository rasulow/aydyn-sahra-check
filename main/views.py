from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import json
import base64

def home(request):
    """Main page view with three sections"""
    return render(request, 'main/home.html')

def sargyt_check(request):
    """Sargyt we check page with data checking form"""
    from .models import Client, Color, Category, Karniz, Selpe, Region, ClientType
    
    # Get all clients with their regions and client types
    clients = Client.objects.select_related('region', 'client_type').all()
    clients_data = [
        {
            'id': client.id,
            'name': client.name,
            'region': client.region.name,
            'client_type': client.client_type.type if client.client_type else None,
            'client_type_id': client.client_type.id if client.client_type else None
        }
        for client in clients
    ]
    
    # Get all regions
    regions = Region.objects.all()
    regions_data = [
        {
            'id': region.id,
            'name': region.name
        }
        for region in regions
    ]
    
    # Get all client types
    client_types = ClientType.objects.all()
    client_types_data = [
        {
            'id': client_type.id,
            'type': client_type.type
        }
        for client_type in client_types
    ]
    
    # Get all colors with price data
    colors = Color.objects.select_related('category').all()
    colors_data = [
        {
            'id': color.id,
            'code': color.kod,
            'category_id': color.category.id if color.category else None,
            'category_name': color.category.name if color.category else None,
            'diller_USD': float(color.diller_USD) if color.diller_USD else 0,
            'diller_TMT': float(color.diller_TMT) if color.diller_TMT else 0,
            'bez_ustanowka_USD': float(color.bez_ustanowka_USD) if color.bez_ustanowka_USD else 0,
            'bez_ustanowka_TMT': float(color.bez_ustanowka_TMT) if color.bez_ustanowka_TMT else 0,
            'mata_USD': float(color.mata_USD) if color.mata_USD else 0,
            'mata_TMT': float(color.mata_TMT) if color.mata_TMT else 0,
        }
        for color in colors
    ]
    
    # Get all karniz options
    karniz_list = Karniz.objects.all()
    karniz_data = [
        {
            'id': karniz.id,
            'name': karniz.name
        }
        for karniz in karniz_list
    ]
    
    # Get all selpe options
    selpe_list = Selpe.objects.all()
    selpe_data = [
        {
            'id': selpe.id,
            'name': selpe.name,
            'price_USD': float(selpe.price_USD),
            'price_TMT': float(selpe.price_TMT)
        }
        for selpe in selpe_list
    ]
    
    # Get all categories
    categories = Category.objects.all()
    categories_data = [
        {
            'id': category.id,
            'name': category.name
        }
        for category in categories
    ]
    
    context = {
        'clients_json': json.dumps(clients_data),
        'colors_json': json.dumps(colors_data),
        'categories_json': json.dumps(categories_data),
        'karniz_json': json.dumps(karniz_data),
        'selpe_json': json.dumps(selpe_data),
        'regions_json': json.dumps(regions_data),
        'client_types_json': json.dumps(client_types_data),
    }
    
    return render(request, 'main/sargyt_check.html', context)

@require_http_methods(["POST"])
def add_client(request):
    """API endpoint to add a new client to the database"""
    from .models import Client, Region, ClientType
    
    try:
        # Get data from request
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        region_id = data.get('region_id')
        client_type_id = data.get('client_type_id')
        
        # Validate required fields
        if not name:
            return JsonResponse({'success': False, 'error': 'Имя пользователя обязательно'}, status=400)
        
        if not region_id:
            return JsonResponse({'success': False, 'error': 'Регион обязателен'}, status=400)
        
        # Check if client already exists
        if Client.objects.filter(name__iexact=name).exists():
            return JsonResponse({'success': False, 'error': 'Пользователь с таким именем уже существует'}, status=400)
        
        # Get region
        try:
            region = Region.objects.get(id=region_id)
        except Region.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Регион не найден'}, status=404)
        
        # Get client type (optional)
        client_type = None
        if client_type_id:
            try:
                client_type = ClientType.objects.get(id=client_type_id)
            except ClientType.DoesNotExist:
                pass
        
        # Create new client
        client = Client.objects.create(
            name=name,
            region=region,
            client_type=client_type,
            wallet=0.0
        )
        
        # Return success with client data
        return JsonResponse({
            'success': True,
            'client': {
                'id': client.id,
                'name': client.name,
                'region': client.region.name
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Неверный формат данных'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def update_wallet(request):
    """API endpoint to update client's wallet based on order items"""
    from decimal import Decimal
    from .models import Client
    
    try:
        data = json.loads(request.body)
        client_id = data.get('client_id')
        order_items = data.get('order_items', [])
        
        if not client_id:
            return JsonResponse({'success': False, 'error': 'Client ID is required'}, status=400)
        
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Client not found'}, status=404)
        
        # Calculate total area from order items
        total_area = Decimal('0.0')
        region_area = Decimal('0.0')
        for item in order_items:
            try:
                width = Decimal(str(item.get('width', 0)))
                height = Decimal(str(item.get('height', 0)))
                quantity = Decimal(str(item.get('quantity', 1)))
                # Use real area sent from frontend for region tracking
                real_area = Decimal(str(item.get('real_area', width * height)))

                # If height*width < 1, multiply the real area by 3
                area_per_item = width * height
                if area_per_item < Decimal('1.0'):
                    area_per_item = area_per_item
                total_area += area_per_item * quantity

                # For region meter square, use the real calculated area without quantity multiplication
                region_area += real_area
            except (TypeError, ValueError, Decimal.InvalidOperation):
                continue
        
        # Update client's wallet (add total_area)
        if total_area > 0:
            wallet_increase = total_area
            client.wallet += wallet_increase
            client.save()

            # Update region's total meter square with real area (not multiplied by quantity)
            region = client.region
            region.total_meter_square += region_area
            region.save()
            
            return JsonResponse({
                'success': True,
                'client_id': client.id,
                'total_area': str(total_area),
                'wallet_increase': str(wallet_increase),
                'new_wallet_balance': str(client.wallet),
                'region_area_added': str(region_area),
                'region_total_meter_square': str(region.total_meter_square)
            })
        
        return JsonResponse({
            'success': True,
            'message': 'No area to add to wallet',
            'client_id': client.id,
            'current_wallet_balance': str(client.wallet)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def save_excel_to_check(request):
    """API endpoint to save Excel file to Check model"""
    from .models import Check
    from datetime import datetime
    
    try:
        # Get data from request
        data = json.loads(request.body)
        file_data = data.get('file_data')  # Base64 encoded file
        file_name = data.get('file_name', f'Sargyt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
        
        if not file_data:
            return JsonResponse({'success': False, 'error': 'Файл не предоставлен'}, status=400)
        
        # Decode base64 file data
        try:
            # Remove data URL prefix if present
            if ',' in file_data:
                file_data = file_data.split(',')[1]
            
            file_content = base64.b64decode(file_data)
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Ошибка декодирования файла: {str(e)}'}, status=400)
        
        # Create Check instance and save file
        check = Check.objects.create()
        check.file.save(file_name, ContentFile(file_content), save=True)
        
        # Return success with check UUID
        response_data = {
            'success': True,
            'check_uuid': str(check.uuid),
            'check_id': check.id,
            'file_url': check.file.url if check.file else None
        }
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Неверный формат данных'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
