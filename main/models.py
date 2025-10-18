from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        

class Region(models.Model):
    name = models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Welayat"
        verbose_name_plural = "Welayatlar"


class Client(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Musderi"
        verbose_name_plural = "Musderiler"


class ClientType(models.Model):
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Musderi gornusi"
        verbose_name_plural = "Musderi gornusleri"


class Currency(models.Model):
    kod = models.CharField(max_length=100, default="TMT")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.kod

    class Meta:
        verbose_name = "Valyuta"
        verbose_name_plural = "Valyutalar"  


class Color(models.Model):
    kod = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    client_type = models.ForeignKey(ClientType, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.kod

    class Meta:
        verbose_name = "Kod renk"
        verbose_name_plural = "Kod renkler"
