from django.shortcuts import render

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
