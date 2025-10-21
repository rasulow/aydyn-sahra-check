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

class ClientType(models.Model):
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Musderi gornusi"
        verbose_name_plural = "Musderi gornusleri"


class Client(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    client_type = models.ForeignKey(ClientType, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.client_type.type if self.client_type else 'Unknown'}"
        

    class Meta:
        verbose_name = "Musderi"
        verbose_name_plural = "Musderiler"


class Color(models.Model):
    kod = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    mary_diller_USD = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    mary_diller_TMT = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    diller_USD = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    diller_TMT = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    bez_ustanowka_USD = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    bez_ustanowka_TMT = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    mata_USD = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    mata_TMT = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.kod

    class Meta:
        verbose_name = "Kod renk"
        verbose_name_plural = "Kod renkler"


class Check(models.Model):
    STATUS_CHOICES = (
        ('inactive', 'Inactive'),
        ('process', 'Process'),
        ('done', 'Done'),
    )
    file = models.FileField(upload_to='checks/', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.client:
            return f"Check #{self.id} - {self.client.name}"
        return f"Check #{self.id}"

    class Meta:
        verbose_name = "Sargyt"
        verbose_name_plural = "Sargytlar"


class Karniz(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Karniz"
        verbose_name_plural = "Karnizler"


class Selpe(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Selpe"
        verbose_name_plural = "Selpeler"
