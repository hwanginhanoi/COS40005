from django.db import models

from django.db import models

class Domain(models.Model):
    title = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Property(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    floor = models.IntegerField()
    bedroom = models.IntegerField()
    toilet = models.IntegerField()
    publish_date = models.DateField()
    contact = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
