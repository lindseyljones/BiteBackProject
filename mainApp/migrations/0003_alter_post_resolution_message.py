# Generated by Django 5.0.2 on 2024-04-28 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_alter_report_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='resolution_message',
            field=models.CharField(default='Problem Has Been Resolved', max_length=40),
        ),
    ]