from django.db import models


class Domain(models.Model):

    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)

    class SelectorType(models.TextChoices):
        XPATH = 'By.XPATH', 'XPath'
        CLASSNAME = 'By.CLASS_NAME', 'Classname'
        CSS_SELECTOR = 'By.CSS_SELECTOR', 'CSS Selector'
        NAME = 'By.NAME', 'Name'
        ID = 'By.ID', 'ID'

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
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)
    bedroom = models.CharField(max_length=255)
    toilet = models.CharField(max_length=255)
    publish_date = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
