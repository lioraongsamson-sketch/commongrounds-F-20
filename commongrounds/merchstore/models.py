from django.db import models
from django.urls import reverse


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    owner = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE
    )
    product_image = models.ImageField()
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(max_digits=10, decimal_place=2)

    status_options = [('Available','Available'),('On sale','On sale'),
                      ('Out of stock','Out of stock')]
    status = models.CharField(
        choices = status_options,
        default ='Available'
    )

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.statue = 'Out of stock'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('merchstore:product_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']
