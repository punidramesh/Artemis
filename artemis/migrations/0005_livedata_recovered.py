# Generated by Django 3.0.5 on 2020-05-16 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artemis', '0004_remove_livedata_recovered'),
    ]

    operations = [
        migrations.AddField(
            model_name='livedata',
            name='recovered',
            field=models.CharField(default='-', max_length=120),
        ),
    ]