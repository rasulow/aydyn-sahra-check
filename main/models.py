from django.db import models

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


class Color(models.Model):
    kod = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.kod

    class Meta:
        verbose_name = "Kod renk"
        verbose_name_plural = "Kod renkler"
