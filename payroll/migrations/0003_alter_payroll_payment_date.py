# Generated by Django 4.2.1 on 2025-01-16 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0002_remove_payroll_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='payment_date',
            field=models.DateField(),
        ),
    ]
