from django.shortcuts import render

def home(request):
    """Main page view with three sections"""
    return render(request, 'main/home.html')

def sargyt_check(request):
    """Sargyt we check page with data checking form"""
    return render(request, 'main/sargyt_check.html')
