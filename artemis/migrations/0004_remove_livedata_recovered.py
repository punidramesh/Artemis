# Generated by Django 3.0.5 on 2020-05-15 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artemis', '0003_delete_countryconfirmedhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livedata',
            name='recovered',
        ),
    ]
