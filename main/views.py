from django.shortcuts import render
import json

def home(request):
    """Main page view with three sections"""
    return render(request, 'main/home.html')

def sargyt_check(request):
    """Sargyt we check page with data checking form"""
    from .models import Client, Color, Currency, ClientType, Category
    
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
    
    # Get all currencies
    currencies = Currency.objects.all()
    currencies_data = [
        {
            'id': currency.id,
            'kod': currency.kod
        }
        for currency in currencies
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
        'currencies_json': json.dumps(currencies_data),
        'client_types_json': json.dumps(client_types_data),
        'categories_json': json.dumps(categories_data),
    }
    
    return render(request, 'main/sargyt_check.html', context)
