from django.shortcuts import render
import json

def home(request):
    """Main page view with three sections"""
    return render(request, 'main/home.html')

def sargyt_check(request):
    """Sargyt we check page with data checking form"""
    from .models import Client, Color, Category, Karniz, Selpe
    
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
    
    # Get all colors with price data
    colors = Color.objects.select_related('category').all()
    colors_data = [
        {
            'id': color.id,
            'code': color.kod,
            'category_id': color.category.id if color.category else None,
            'category_name': color.category.name if color.category else None,
            'mary_diller_USD': float(color.mary_diller_USD) if color.mary_diller_USD else 0,
            'mary_diller_TMT': float(color.mary_diller_TMT) if color.mary_diller_TMT else 0,
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
            'price': float(selpe.price)
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
    }
    
    return render(request, 'main/sargyt_check.html', context)
