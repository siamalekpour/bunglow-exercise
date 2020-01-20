import logging
import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from homes.models import Country, State, HomeType, Home


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def get_field_value(self, header, row, field):
        """ Find field index in header

        And use that index to find field value. This prevents errors in case the CSV fiel's format
        changes in the future
        """
        index = header.index(field)
        value = row[index]

        if value == '':
            value = None

        return value

    def get_date_field_value(self, *args, **kwargs):
        """ Read field value for dates

        calls `self.get_field_value` but then converts the string to a date format
        """
        value = self.get_field_value(*args, **kwargs)
        if value is not None:
            value = datetime.strptime(value, '%m/%d/%Y')
        return value

    def convert_price_to_int(self, value):
        """ Convert price from human readable format to integer

        Prices in our csv have a dollar sign and are shortened to decimals post-fixed with their shorthand character
        e.g. 1,500,000 is store as $1.5M
        """

        multiplier = 1

        # Remove dollar sign
        price = value.replace('$', '')

        thousands_index = price.find('K')
        millions_index = price.find('M')
        billions_index = price.find('B')

        if thousands_index > 0:
            multiplier = 1000
            price = price.replace('K', '')
        elif millions_index > 0:
            multiplier = 1000000
            price = price.replace('M', '')
        elif billions_index > 0:
            multiplier = 1000000000
            price = price.replace('B', '')

        return int(float(price) * multiplier)

    def handle(self, *args, **options):
        with open('../challenge_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            counter = 0
            header = None
            country = Country.objects.get(code='US')

            for row in csv_reader:
                if counter == 0:
                    header = row

                else:
                    # TODO: state

                    home = Home()
                    home.area_unit = self.get_field_value(header, row, 'area_unit')
                    home.bathrooms = self.get_field_value(header, row, 'bathrooms')
                    home.bedrooms = self.get_field_value(header, row, 'bedrooms')
                    home.home_size = self.get_field_value(header, row, 'home_size')

                    home_type = self.get_field_value(header, row, 'home_type')
                    home.home_type = HomeType.objects.get_or_create(name=home_type)[0]
                    home.last_sold_date = self.get_date_field_value(header, row, 'last_sold_date')
                    home.last_sold_price = self.get_field_value(header, row, 'last_sold_price')
                    home.link = self.get_field_value(header, row, 'link')

                    price = self.get_field_value(header, row, 'price')
                    home.price = self.convert_price_to_int(price)

                    home.property_size = self.get_field_value(header, row, 'property_size')
                    home.rent_price = self.get_field_value(header, row, 'rent_price')
                    home.rentzestimate_amount = self.get_field_value(header, row, 'rentzestimate_amount')

                    home.rentzestimate_last_updated = self.get_date_field_value(header, row, 'rentzestimate_last_updated')

                    tax_value = self.get_field_value(header, row, 'tax_value')
                    home.tax_value = int(float(tax_value))

                    home.tax_year = self.get_field_value(header, row, 'tax_year')
                    home.year_built = self.get_field_value(header, row, 'year_built')
                    home.zestimate_amount = self.get_field_value(header, row, 'zestimate_amount')
                    home.zestimate_last_updated = self.get_date_field_value(header, row, 'zestimate_last_updated')
                    home.zillow_id = self.get_field_value(header, row, 'zillow_id')
                    home.address = self.get_field_value(header, row, 'address')
                    home.city = self.get_field_value(header, row, 'city')

                    # TODO: Since there is no actual country/state tables,
                    #       I'm assuming all states are California for this challenge
                    # state = self.get_field_value(header, row, 'state')
                    state = State.objects.first()
                    home.state = State.objects.get_or_create(name=state, country=country)[0]

                    # home.zipcode = self.get_field_value(header, row, 'zipcode')
                    home.zipcode = '10'

                    home.save()
                    print('{} - Created home w/ zillow id: {}'.format(counter, home.zillow_id))

                counter += 1

            print(f'Processed {counter} homes.')
