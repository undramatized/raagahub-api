# Generated by Django 3.0.5 on 2020-05-23 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raagaapi', '0002_chord'),
    ]

    operations = [
        migrations.AddField(
            model_name='raga',
            name='aliases',
            field=models.CharField(blank=True, max_length=10000),
        ),
    ]
