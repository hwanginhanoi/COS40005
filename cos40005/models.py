from django.db import models


class Domain(models.Model):
    title = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    pagination = models.CharField(max_length=255, default='')

    title_classname = models.CharField(max_length=255, default='')
    price_classname = models.CharField(max_length=255, default='')
    address_classname = models.CharField(max_length=255, default='')

    area_xpath = models.CharField(max_length=255, default='')
    bedroom_xpath = models.CharField(max_length=255, default='')
    toilet_xpath = models.CharField(max_length=255, default='')
    publish_date_xpath = models.CharField(max_length=255, default='')

    description_classname = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.title


class Cache(models.Model):
    title = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='caches')
    url = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.url


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
