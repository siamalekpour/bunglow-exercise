from django.contrib.humanize.templatetags.humanize import intword
from django.db import models

from .validators import validate_year
from .constants import AreaUnit


class Country(models.Model):
    code = models.CharField(
        max_length=2,
        primary_key=True,
        help_text='Stores the two letter "Alpha-2" country code'
    )
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'homes'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'homes'

    def __str__(self):
        return self.name


class HomeType(models.Model):
    # TODO: if the data in this table doesn't grow,
    #       might've been better as a choices field instead of a separate model
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'homes'

    def __str__(self):
        return self.name


class Home(models.Model):

    home_type = models.ForeignKey(HomeType, on_delete=models.SET_NULL, blank=True, null=True)

    area_unit = models.CharField(
        max_length=4,
        choices=AreaUnit.CHOICES,
        default=AreaUnit.SQUARE_FEET,
        blank=True,
        null=True,
    )
    home_size = models.PositiveIntegerField(blank=True, null=True)
    property_size = models.PositiveIntegerField(blank=True, null=True)
    year_built = models.PositiveSmallIntegerField(validators=[validate_year], blank=True, null=True)

    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    bedrooms = models.PositiveSmallIntegerField(blank=True, null=True)

    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    # TODO: zipcode validator that supports different countries
    zip_code = models.CharField(max_length=10)

    # Price values are large. Cents are not important
    price = models.PositiveIntegerField(blank=True, null=True)
    last_sold_price = models.PositiveIntegerField(blank=True, null=True)
    last_sold_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)

    rent_price = models.PositiveIntegerField(blank=True, null=True)
    
    zestimate_amount = models.PositiveIntegerField(blank=True, null=True)
    zestimate_last_updated = models.DateField(blank=True, null=True)

    rentzestimate_amount = models.PositiveIntegerField(blank=True, null=True)
    rentzestimate_last_updated = models.DateField(blank=True, null=True)

    tax_value = models.PositiveIntegerField(blank=True, null=True)
    tax_year = models.PositiveSmallIntegerField(validators=[validate_year], blank=True, null=True)

    # TODO: Is the zillow id unique in our db?
    #       Add `unique=True` if they can be`
    zillow_id = models.PositiveIntegerField(blank=True, null=True)
    link = models.URLField(max_length=500,blank=True, null=True, help_text='Link to Zillow ad')

    class Meta:
        app_label = 'homes'

    @property
    def readable_price(self):
        return intword(self.price)

    @property
    def readable_last_sold_price(self):
        return intword(self.last_sold_price)

    @property 
    def readable_rent_price(self):
        return intword(self.rent_price)

    @property 
    def readable_rentzestimate_amount(self):
        return intword(self.rentzestimate_amount)

    @property 
    def readable_tax_value(self):
        return intword(self.tax_value)
