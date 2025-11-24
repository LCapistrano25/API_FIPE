from django.db import models

class FipeCar(models.Model):
    fipe_id = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=255)
    gear_type = models.CharField(max_length=255)
    engine_size = models.FloatField()
    price = models.FloatField()

    class Meta:
        db_table = 'tb_fipe_car'
        verbose_name = 'Fipe Car'
        verbose_name_plural = 'Fipe Cars'
        
    def __str__(self):
        return f'{self.brand} {self.model} {self.year}'