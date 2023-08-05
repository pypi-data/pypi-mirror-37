from django.db import models


class WeatherStation(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return 'DISPLAY FIELD CONTENT'


class TemperatureRecord(models.Model):
    class Meta:
        unique_together = ('station', 'date')

    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE)
    date = models.DateField()
    temperature = models.DecimalField(decimal_places=3, max_digits=6)
