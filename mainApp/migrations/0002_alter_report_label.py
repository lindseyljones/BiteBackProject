# Generated by Django 5.0.2 on 2024-04-28 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='label',
            field=models.CharField(choices=[('Inaccurate', 'Inaccurate'), ('Problem is Resolved', 'Problem is Resolved')], default='Inaccurate', max_length=40),
        ),
    ]
