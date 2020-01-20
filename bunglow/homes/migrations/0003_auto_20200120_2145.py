# Generated by Django 2.2.9 on 2020-01-20 21:45

from django.db import migrations


def create_states(apps, schema_editor):
    Country = apps.get_model('homes', 'Country')
    State = apps.get_model('homes', 'State')

    country = Country.objects.create(code='US', name='United States of America')
    State.objects.create(country=country, name='CA')


class Migration(migrations.Migration):

    dependencies = [
        ('homes', '0002_auto_20200120_2116'),
    ]

    operations = [
        migrations.RunPython(create_states)
    ]