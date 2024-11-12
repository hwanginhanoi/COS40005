from django.db import models
from selenium.webdriver.common.by import By


class Domain(models.Model):

    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    enable = models.BooleanField(default=False)

    class SelectorType(models.TextChoices):
        XPATH = By.XPATH, 'XPath'
        CLASSNAME = By.CLASS_NAME, 'Classname'
        CSS_SELECTOR = By.CSS_SELECTOR, 'CSS Selector'
        NAME = By.NAME, 'Name'
        ID = By.ID, 'ID'

    title_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    title_property = models.CharField(max_length=255, null=True, blank=True)

    address_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    address_property = models.CharField(max_length=255, null=True, blank=True)

    price_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    price_property = models.CharField(max_length=255, null=True, blank=True)

    area_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    area_property = models.CharField(max_length=255, null=True, blank=True)

    floor_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    floor_property = models.CharField(max_length=255, null=True, blank=True)

    bedroom_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    bedroom_property = models.CharField(max_length=255, null=True, blank=True)

    toilet_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    toilet_property = models.CharField(max_length=255, null=True, blank=True)

    publish_date_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    publish_date_property = models.CharField(max_length=255, null=True, blank=True)

    contact_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    contact_property = models.CharField(max_length=255, null=True, blank=True)

    description_type = models.CharField(
        max_length=20,
        choices=SelectorType.choices,
        null=True,
        blank=True
    )
    description_property = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Cache(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='caches')
    url = models.CharField(max_length=255, unique=True)
    status = models.BooleanField(default=False)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return self.url


class Property(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=2048)
    # url = models.CharField(max_length=2048)
    address = models.CharField(max_length=2048, null=True, blank=True)
    price = models.CharField(max_length=2048)
    area = models.CharField(max_length=2048, null=True, blank=True)
    floor = models.CharField(max_length=2048, null=True, blank=True)
    bedroom = models.CharField(max_length=2048, null=True, blank=True)
    toilet = models.CharField(max_length=2048, null=True, blank=True)
    publish_date = models.CharField(max_length=2048, null=True, blank=True)
    contact = models.CharField(max_length=2048, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class ExtractedProperty(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='extracted_properties')
    title = models.CharField(max_length=2048)
    # url = models.CharField(max_length=2048)
    address = models.CharField(max_length=2048, null=True, blank=True)
    price = models.CharField(max_length=2048)
    area = models.CharField(max_length=2048, null=True, blank=True)
    floor = models.CharField(max_length=2048, null=True, blank=True)
    bedroom = models.CharField(max_length=2048, null=True, blank=True)
    toilet = models.CharField(max_length=2048, null=True, blank=True)
    publish_date = models.CharField(max_length=2048, null=True, blank=True)
    contact = models.CharField(max_length=2048, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title

class DataExport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    file_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Data Export'
        verbose_name_plural = 'Data Exports'

